from UserServices.models import Users
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class SignupAPIView(APIView):
    def get(self, request):
        return Response({"message":"get request is not accepted"})

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        phone = request.data.get("phone")

        if username is None or email is None or password is None or phone is None:
            print(username, email)
            return Response({"error": "Please provide username, email, phone, and password"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = Users.objects.create_user(username=username, email=email, password=password, phone=phone)
        user.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access["username"] = user.username
        access["email"] = user.email
        access["phone"] = user.phone
        

        return Response({"access":str(access), "refresh" :str(refresh), "message": "User created successfully"}, status=status.HTTP_201_CREATED)

"""
Login API.

This API is used to login a user to the system.

Parameters:
username (str): The username of the user.
password (str): The password of the user.

Returns:
Response: A response containing a refresh token and an access token.

Raises:
Response: A response with status code 400 if the username or password is not provided.
Response: A response with status code 401 if the credentials are invalid.
"""
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None and password is None:
            return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST,)
        
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            access["username"] = user.username
            access["email"] = user.email
            access["phone"] = user.phone

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


    def get(self, request):
        """
        GET /auth/login/
        
        Returns a message to tell the user to use the POST method to login
        """
        return Response({"message":"please use Post method to login"}) 
    

class PublicAPIView(APIView):
    def get(self, request):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        return Response({"message":f'Your IP address is: {ip_address}'})

class ProtectedAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response({"message": "This is protected API."})  
