from django.urls import path

from endpoints.services.api.service_api import CreateServiceRequestAPIView

urlpatterns = [
    path("create/request", CreateServiceRequestAPIView.as_view()),
]
