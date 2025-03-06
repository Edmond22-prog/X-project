from django.db import models

from app_models.models.user import User
from app_models.models.constants import ServiceRequestStatus, SERVICE_REQUEST_STATUS
from utils.common import generate_uuid


class ServiceRequest(models.Model):
    uuid = models.CharField(
        max_length=100, default=generate_uuid, editable=False, primary_key=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="service_requests"
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=SERVICE_REQUEST_STATUS,
        default=ServiceRequestStatus.ACTIVE,
    )
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    duration = models.IntegerField()  # In days
    fixed_amount = models.IntegerField()  # In FCFA

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ServiceProposalSkill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ServiceProposalCategory(models.Model):
    uuid = models.CharField(
        max_length=100, default=generate_uuid, editable=False, primary_key=True
    )
    fr_name = models.CharField(max_length=50, unique=True)
    fr_description = models.TextField()
    en_name = models.CharField(max_length=50, unique=True)
    en_description = models.TextField()

    def __str__(self):
        return f"{self.fr_name} | {self.en_name}"


class ServiceProposal(models.Model):
    uuid = models.CharField(
        max_length=100, default=generate_uuid, editable=False, primary_key=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="services")

    title = models.CharField(max_length=100)
    description = models.TextField()
    hourly_rate = models.IntegerField()  # In FCFA
    skills = models.ManyToManyField(ServiceProposalSkill)
    category = models.ForeignKey(
        ServiceProposalCategory,
        on_delete=models.SET_NULL,
        related_name="proposals",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
