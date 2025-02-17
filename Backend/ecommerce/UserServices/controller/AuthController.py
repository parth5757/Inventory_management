import os
from django.conf import settings
from django.core.files.storage import default_storage
from UserServices.models import Users
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import re
import phonenumbers
from random import randint
import face_recognition
from UserServices.task import send_otp_handler
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
import time
from ecommerce.Helpers import renderResponse
from ecommerce.permission import IsSuperAdmin

# Function to create necessary directories
def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to suggest unique usernames
def suggest_username(username):
    suggestions = []
    for i in range(120):
        new_username = f"{username}{randint(1000, 9999)}"
        if not Users.objects.filter(username=new_username).exists():
            suggestions.append(new_username)
    return suggestions

# Function to check if profile image has a single unobstructed face
def is_single_unobstructed_face(image_path):
    if not os.path.exists(image_path):
        return False
    image = face_recognition.load_image_file(image_path)
    face_landmarks_list = face_recognition.face_landmarks(image)

    if len(face_landmarks_list) != 1:
        return False
    
    face_landmarks = face_landmarks_list[0]
    if not ('left_eye' in face_landmarks and 'right_eye' in face_landmarks and 
            'nose_tip' in face_landmarks and 'top_lip' in face_landmarks and 'bottom_lip' in face_landmarks):
        return False

    return True

# Compare uploaded image with existing users' profile pictures
def compare_with_existing_users_profile_pics(uploaded_image_path):
    if not os.path.exists(uploaded_image_path):
        return False, []  # No file to process

    uploaded_image = face_recognition.load_image_file(uploaded_image_path)
    uploaded_image_encodings = face_recognition.face_encodings(uploaded_image)

    if not uploaded_image_encodings:
        return False, []  # No face detected in uploaded image

    uploaded_image_encoding = uploaded_image_encodings[0]

    matches = []
    for user in Users.objects.exclude(profile_pic="").all():
        known_image_path = user.profile_pic.path
        if not os.path.exists(known_image_path):
            continue

        known_image = face_recognition.load_image_file(known_image_path)
        known_image_encodings = face_recognition.face_encodings(known_image)

        if not known_image_encodings:
            continue

        known_image_encoding = known_image_encodings[0]
        face_distance = face_recognition.face_distance([known_image_encoding], uploaded_image_encoding)[0]
        match_percentage = (1 - face_distance) * 100

        if match_percentage > 50:
            matches.append((user.username, match_percentage))

    return True if matches else False, matches

# API for user signup
class SignupAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        phone = request.data.get("phone")
        profile_pic = request.FILES.get("profile_pic")

        # Check same email is exist or not
        emailCheck = Users.objects.filter(email=email)
        if emailCheck.exists():
            return renderResponse(data= "email is already exists", message='email is already exists', status=status.HTTP_400_BAD_REQUEST)
            # return Response({"error": "email is already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check same phone number is exist or not
        phoneCheck = Users.objects.filter(phone=phone)
        if phoneCheck.exists():
            return Response({"error": "phone already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate required fields
        if not all([username, email, password, phone]):
            return Response({"error": "Please provide username, email, phone, and password"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username is available
        if Users.objects.filter(username=username).exists():
            suggestions = suggest_username(username)
            return Response({"error": "Username not available", "suggestions": suggestions}, status=status.HTTP_409_CONFLICT)

        # Password validation
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            return Response({"error": "Password does not meet requirements."}, status=status.HTTP_400_BAD_REQUEST)

        # Phone validation
        try:
            parsed_phone = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(parsed_phone):
                return Response({"error": "Invalid phone number."}, status=status.HTTP_400_BAD_REQUEST)
        except phonenumbers.NumberParseException:
            return Response({"error": "Invalid phone number format."}, status=status.HTTP_400_BAD_REQUEST)

        # Temporarily save profile_pic if provided and check for matching faces
        if profile_pic:
            # Ensure media directory and path for profile_pic
            media_path = settings.MEDIA_ROOT
            ensure_directory_exists(media_path)

            temp_profile_pic_path = os.path.join(media_path, profile_pic.name)
            with default_storage.open(temp_profile_pic_path, 'wb+') as destination:
                for chunk in profile_pic.chunks():
                    destination.write(chunk)

            # Check if uploaded image has a single, unobstructed face
            if not is_single_unobstructed_face(temp_profile_pic_path):
                return Response({"error": "The profile picture does not show a single, unobstructed face."}, status=status.HTTP_400_BAD_REQUEST)

            # Compare uploaded profile picture with existing users' profile pictures
            is_match, matched_users = compare_with_existing_users_profile_pics(temp_profile_pic_path)
            if is_match:
                matches_info = [f"{username} ({match_percentage:.2f}%)" for username, match_percentage in matched_users]
                return Response({"error": "Profile picture matches existing users", "matches": matches_info}, status=status.HTTP_409_CONFLICT)

        # Create new user if no match is found
        user = Users.objects.create_user(username=username, email=email, password=password, phone=phone)
        if request.data.get('domain_user_id'):
            user.domain_user_id = Users.objects.get(id=request.data.get('domain_user_id'))
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()

        # Generate tokens and respond
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access["email"] = user.email

        send_otp_handler.delay(user.email)


        return Response(
            {
                "access": str(access), 
                "refresh": str(refresh), 
                "message": "User created successfully",
                # "SE": request.session.get("email")
            }, 
            status=status.HTTP_201_CREATED)

class OTPVerifyEmailView(APIView):
    # # to get all email which are currently in cache memory
    def get(self, request):
        # Construct cache key and fetch email from cache
        # cache_key = 'wagag98069@kurbieh.com' # add your If any specific email you want to searchs
        # otp = cache.get(cache_key)

        keys = cache.keys('*')
        if not keys:
            return Response({"error":"no data found"}, status=status.HTTP_404_NOT_FOUND)

        all_cache_data = {key: cache.get(key) for key in keys}
        # otp_from_cache = cache.get(cache_key)
        return Response(all_cache_data)

    def post(self, request):
        print("OTP request received")
        # Retrieve email and OTP from request data
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not otp:
            return Response({"error": "OTP is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Construct cache key and fetch email from cache and get otp of that email. Validate email and make user is_verify True
        otp_from_cache = cache.get(email)

        if otp_from_cache is None:
            return Response({"error": "Invalid or expired otp"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate otp
        if str(otp_from_cache) == str(otp):
            try:
                # Update User Verification status
                user = Users.objects.get(email=email)
                user.is_verify = True
                user.save()

                # Clear the OTP from cache memory
                cache.delete(email)

                return Response({"verified": "User verify successfully"})
            except Users.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error":f"An unexpected error occurred {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @method_decorator(ratelimit(key="post:email:{email}", rate="1/2m", method="POST", block=True), name='dispatch')
class ResendOTPEmailView(APIView):
    # @ratelimit(key="post:email", rate="1/2m", method=("POST",), block=True)
    def post(self, request):
        # Retrieve email data
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the email is in cache (rate limit per unique email)
        cache_key = email
        last_request_time = cache.ttl(cache_key)
        if last_request_time > 180:
            return Response({"error": "You can request OTP only once every 2 minutes."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Store the email in cache for 2 minutes (120 seconds)
        cache.set(cache_key, time.time(), timeout=120)

        # Check same email is exist or not
        user = Users.objects.filter(email=email)
        if user.exists():
            # email verified or not
            user = Users.objects.filter(email=email).first()
            if(user.is_verify):
                return Response({'message': 'user is already verified'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                send_otp_handler.delay(email)
                return Response({'success': f'OTP Resend successfully on {email}'}, status=status.HTTP_200_OK)
            
        else:
            print("Email does not exists")
            return Response({"error": "Email is not exist."}, status=status.HTTP_400_BAD_REQUEST) 
        
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None and password is None:
            return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            # Adding custom claims
            access["email"] = user.email

            if not user.is_verify:
                send_otp_handler.delay(user.email)
                return Response({
                    'verify': "Your email is not verified. Please verify your email before logging in.",
                    'ET': str(access),
                })                

            # Adding custom claims
            access["username"] = user.username
            access["phone"] = user.phone


            return Response({
                'refresh': str(refresh),
                'access': str(access),
            })

        else:
            return Response({
                'permission': str("Not Allowed"),
                'error': str("Invalid credentials"),
            })

# just for personal test
class PublicAPIView(APIView):
    def get(self, request):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        return Response({"message": f'Your IP address is: {ip_address}'})


class ProtectedAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected API."})
    
class SuperAdminCheckAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    def get(self, request):
        return Response({"message": "This is a SuperAdmin API."})

# just for personal test
class Test(APIView):
    def get(self, request):
        # test_fun.delay()
        email = "me@parththakkar.in"
        send_otp_handler.delay(email)
        return Response({"Otp sended on given email"})

# celery -A ecommerce.celery worker --pool=solo -l info