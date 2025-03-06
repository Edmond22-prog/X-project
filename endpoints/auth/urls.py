from django.urls import path

from endpoints.auth.api.auth_api import LoginAPIView, RefreshAPIView

urlpatterns = [
    path("login", LoginAPIView.as_view()),
    path("refresh", RefreshAPIView.as_view()),
]
