from django.urls import path

from endpoints.auth.api.auth_api import LoginAPIView, RefreshAPIView
from endpoints.auth.api.user_api import (
    ConnectedUserAPIView,
    GetUserProfileAPIView,
    RegisterUserAPIView,
    UserVerificationAPIView,
)

urlpatterns = [
    path("auth/login", LoginAPIView.as_view()),
    path("auth/refresh", RefreshAPIView.as_view()),
    path("users/register", RegisterUserAPIView.as_view()),
    path("users/verify", UserVerificationAPIView.as_view()),
    path("auth/current-user/", ConnectedUserAPIView.as_view()),
    path("users/<str:user_uuid>/profile/", GetUserProfileAPIView.as_view()),
]
