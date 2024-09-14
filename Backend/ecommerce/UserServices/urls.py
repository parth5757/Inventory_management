from django.urls import path, include
from .controller import AuthController

urlpatterns = [
    path("login/", AuthController.LoginAPIView.as_view(), name="login"),
    path("publicapi/", AuthController.PublicAPIView.as_view(), name="publicApi"),
    path("protectedapi/", AuthController.ProtectedAPIView.as_view(), name="protectedApi"),
]
