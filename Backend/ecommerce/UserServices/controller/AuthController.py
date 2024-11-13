# from UserServices.models import Users
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# import re
# import phonenumbers
# from random import randint

# # Suggest username while user signing up
# def suggest_username(username):
#     suggestions = []
#     for i in range(5):
#         new_username = f"{username}{randint(100,999)}"
#         if not Users.objects.filter(username=new_username).exists():
#             suggestions.append(new_username)
#     return suggestions

# # user signup api logic
# class SignupAPIView(APIView):
#     def get(self, request):
#         return Response({"message":"get request is not accepted"})

#     # posting entered user details to server with checking all validation
#     def post(self, request):    
#         username = request.data.get("username")
#         email = request.data.get("email")
#         password = request.data.get("password")
#         phone = request.data.get("phone")
#         profile_pic = request.FILES.get("profile_pic")  # Use FILES to get uploaded file

#         # Validation for missing fields
#         if not all([username, email, password, phone]):
#             return Response({"error": "Please provide username, email, phone, and password"}, status=status.HTTP_400_BAD_REQUEST)

#         # checking user exist or not
#         if Users.objects.filter(username=username).exists():
#             suggestions = suggest_username(username)
#             return Response({"error": "Username not available", "suggestions": suggestions}, status=status.HTTP_409_CONFLICT)
        
#         # Password validation
#         if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
#             return Response({"error": "Password must be at least 8 characters long, include one uppercase letter, one lowercase letter, one special character, and one number."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Phone Validation
#         '''check from react inventory app chat (work is going not include the react phone library because of design issue 
#         # https://www.youtube.com/watch?v=nUyWNTqu2p4&t=1410s
#         https://chatgpt.com/c/6713b1db-7094-8000-8571-473fe730387f)'''

#         try:
#             parsed_phone = phonenumbers.parse(phone, None)
#             if not phonenumbers.is_valid_number(parsed_phone):
#                 return Response({"error":"Invalid Phone number ."}, status=status.HTTP_400_BAD_REQUEST)
#         except phonenumbers.NumberParseException:
#             return Response({"error":"Invalid phone number format."}, status=status.HTTP_400_BAD_REQUEST)

            
#         # create user
#         user = Users.objects.create_user(username=username, email=email, password=password, phone=phone)
#         if profile_pic:
#             user.profile_pic = profile_pic
#         user.save()

#         refresh = RefreshToken.for_user(user)
#         access = refresh.access_token
#         access["username"] = user.username
#         access["email"] = user.email
#         access["phone"] = user.phone
        

#         return Response({"access":str(access), "refresh" :str(refresh), "message": "User created successfully"}, status=status.HTTP_201_CREATED)

# """
# Login API.

# This API is used to login a user to the system.

# Parameters:
# username (str): The username of the user.
# password (str): The password of the user.

# Returns:
# Response: A response containing a refresh token and an access token.

# Raises:
# Response: A response with status code 400 if the username or password is not provided.
# Response: A response with status code 401 if the credentials are invalid.
# """
# class LoginAPIView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if username is None and password is None:
#             return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST,)
        
#         user = authenticate(request, username=username, password=password)
#         if user:
#             refresh = RefreshToken.for_user(user)
#             access = refresh.access_token
#             access["username"] = user.username
#             access["email"] = user.email
#             access["phone"] = user.phone

#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 })
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


#     def get(self, request):
#         """
#         GET /auth/login/
        
#         Returns a message to tell the user to use the POST method to login
#         """
#         return Response({"message":"please use Post method to login"}) 
    

# class PublicAPIView(APIView):
#     def get(self, request):
#         ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
#         if ip_address:
#             ip_address = ip_address.split(',')[0]
#         else:
#             ip_address = request.META.get('REMOTE_ADDR')
#         return Response({"message":f'Your IP address is: {ip_address}'})

# class ProtectedAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self,request):
#         return Response({"message": "This is protected API."})  





# Not working image checking code
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
import re
import phonenumbers
from random import randint
import face_recognition

# Function to create necessary directories
def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to suggest unique usernames
def suggest_username(username):
    suggestions = []
    for i in range(5):
        new_username = f"{username}{randint(100, 999)}"
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
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()

        # Generate tokens and respond
        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh), "message": "User created successfully"}, status=status.HTTP_201_CREATED)



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
            access["username"] = user.username
            access["email"] = user.email
            access["phone"] = user.phone
                

            return Response({
                'refresh': str(refresh),
                'access': str(access),
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


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

