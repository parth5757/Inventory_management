from UserServices.models import Users
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class SignupAPIView(APIVIEW):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        profile_pic = request.data.get("profile_pic")

        if username is None or email is None or password is None or profile_pic is None:
            return Response({"error": "Please provide username, email and password"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = Users.objects.create_user(username=username, email=email, password=password, profile_pic=profile_pic)
        user.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access[username] = user.username
        access[email] = user.email
        access[profile_pic] = user.profile_pic
        

        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

        # check at 27:00 minute

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
            access["profile_pic"] = user.profile_pic

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response({"message":"please use Post method to login"})
    

class PublicAPIView(APIView):
    def get(self, request):
        return Response({"message":"this is publicly accessible api"})

class ProtectedAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response({"message": "This is protected API."})
