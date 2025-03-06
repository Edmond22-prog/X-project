from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer,
    RefreshJSONWebTokenSerializer,
)
from rest_framework_jwt.settings import api_settings

from app_models.models.user import User
from backend.settings import TOKEN_VALIDITY


class LoginSerializer(JSONWebTokenSerializer):
    def custom_jwt_encode_handler(self, payload):
        return api_settings.JWT_ENCODE_HANDLER(payload)

    def custom_jwt_payload_handler(self, user):
        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
        # Add custom fields to the payload
        payload["phone"] = user.phone
        payload["exp"] = datetime.utcnow() + timedelta(minutes=TOKEN_VALIDITY)

        return payload

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # Check if email_or_phone is an email or phone
        if "@" in username:
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(phone=username).first()

        # Check if user exists and password is correct
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid email/phone or password")

        # Set the user username to the attrs
        attrs["username"] = user.username

        # Call the parent class's validate method to get the token
        data = super(LoginSerializer, self).validate(attrs)
        payload = self.custom_jwt_payload_handler(data["user"])
        return {"token": self.custom_jwt_encode_handler(payload)}


class RefreshSerializer(RefreshJSONWebTokenSerializer):
    def custom_jwt_encode_handler(self, payload):
        return api_settings.JWT_ENCODE_HANDLER(payload)

    def custom_jwt_payload_handler(self, user):
        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
        # Add custom fields to the payload
        payload["phone"] = user.phone
        payload["exp"] = datetime.utcnow() + timedelta(minutes=TOKEN_VALIDITY)

        return payload

    def validate(self, attrs):
        data = super(RefreshSerializer, self).validate(attrs)

        payload = self.custom_jwt_payload_handler(data["user"])
        return {"token": self.custom_jwt_encode_handler(payload)}
