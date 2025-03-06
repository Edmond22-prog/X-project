from django.db import models

from app_models.models.service import ServiceRequest
from app_models.models.user import User


class UserSocials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="socials")
    whatsapp = models.CharField(max_length=20, null=True, default=None)
    telegram = models.CharField(max_length=20, null=True, default=None)

    def __str__(self):
        return f"Socials of {self.user.get_full_name()}"


class ServiceRequestSocials(models.Model):
    service_request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name="contacts"
    )
    email = models.EmailField(null=True, default=None)
    phone = models.CharField(max_length=20, null=True, default=None)
    whatsapp = models.CharField(max_length=20, null=True, default=None)
    telegram = models.CharField(max_length=20, null=True, default=None)

    def __str__(self):
        return f"Contacts for {self.service_request.title}"
