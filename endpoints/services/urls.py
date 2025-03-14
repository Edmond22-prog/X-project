from django.urls import path

from endpoints.services.api.service_api import (
    CreateServiceProposalAPIView,
    CreateServiceRequestAPIView,
    GetServiceRequestAPIView,
    PaginatedServiceProposalsAPIView,
    PaginatedServiceRequestsAPIView,
    RetrieveCategoriesAPIView,
    RetrieveSkillsAPIView,
    UpdateServiceRequestAPIView,
)

urlpatterns = [
    path("create/request", CreateServiceRequestAPIView.as_view()),
    path("requests/list/", PaginatedServiceRequestsAPIView.as_view()),
    path("requests/<str:service_request_uuid>/get/", GetServiceRequestAPIView.as_view()),
    path("skills/", RetrieveSkillsAPIView.as_view()),
    path("categories/", RetrieveCategoriesAPIView.as_view()),
    path("create/proposal", CreateServiceProposalAPIView.as_view()),
    path("proposals/list/", PaginatedServiceProposalsAPIView.as_view()),
    path("update/request/<str:request_uuid>/", UpdateServiceRequestAPIView.as_view()),
]
