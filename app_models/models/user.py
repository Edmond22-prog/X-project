from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.common import generate_uuid


class User(AbstractUser):
    REQUIRED_FIELDS = []

    uuid = models.CharField(
        max_length=100, default=generate_uuid, editable=False, primary_key=True
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, null=True, default=None)
    phone = models.CharField(max_length=20, unique=True, null=True, default=None)
    username = models.CharField(
        max_length=50, unique=True, null=True, default=None, editable=False
    )
    city = models.CharField(max_length=100, null=True, default=None)
    district = models.CharField(max_length=100, null=True, default=None)

    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.email:
            self.username = self.phone
        else:
            self.username = self.email

        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()


class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_photo = models.ImageField(upload_to="verification_photos/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "user verification"
        verbose_name_plural = "Users Verifications"

    def __str__(self):
        return f"Verification photo for {self.user.get_full_name()}"
