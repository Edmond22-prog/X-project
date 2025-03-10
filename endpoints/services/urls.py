from django.urls import path

from endpoints.services.api.service_api import (
    CreateServiceRequestAPIView,
    GetServiceRequestAPIView,
    PaginatedServicesRequestsAPIView,
    RetrieveSkillsAPIView,
)

urlpatterns = [
    path("create/request", CreateServiceRequestAPIView.as_view()),
    path("requests/list/", PaginatedServicesRequestsAPIView.as_view()),
    path("requests/<str:service_request_uuid>/get/", GetServiceRequestAPIView.as_view()),
    path("skills/", RetrieveSkillsAPIView.as_view()),
]
