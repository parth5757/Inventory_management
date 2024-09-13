from django.urls import path, include
from .controller import AuthController

urlpatterns = [
    path("login/", AuthController.LoginAPIView.as_view(), name="login"),
]
