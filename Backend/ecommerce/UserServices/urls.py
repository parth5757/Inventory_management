from django.urls import path, include
from .controller import AuthController

urlpatterns = [
    path("login/", AuthController.LoginAPIView.as_view(), name="login"),
    path("publicapi/", AuthController.PublicAPIView.as_view(), name="publicApi"),
    path("protectedapi/", AuthController.ProtectedAPIView.as_view(), name="protectedApi"),
    path("signup/", AuthController.SignupAPIView.as_view(), name="signup"),
    path("verify-email/", AuthController.OTPVerifyEmailView.as_view(), name="get-email"),
    path("resend_otp/", AuthController.ResendOTPEmailView.as_view(), name="resend_email"),
    path("test_celery", AuthController.Test.as_view(), name="test_celery")
]
