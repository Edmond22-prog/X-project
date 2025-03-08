from django.urls import path

from endpoints.auth.api.auth_api import LoginAPIView, RefreshAPIView
from endpoints.auth.api.user_api import (
    ConnectedUserAPIView,
    RegisterUserAPIView,
    UserVerificationAPIView,
)

urlpatterns = [
    path("login", LoginAPIView.as_view()),
    path("refresh", RefreshAPIView.as_view()),
    path("users/register", RegisterUserAPIView.as_view()),
    path("users/verify", UserVerificationAPIView.as_view()),
    path("users/current/", ConnectedUserAPIView.as_view()),
]
