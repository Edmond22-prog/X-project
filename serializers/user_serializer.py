from rest_framework import serializers

from app_models.models import User, UserSocials
from serializers.service_serializer import (
    ServiceProposalSerializer,
    ServiceRequestSerializer,
)


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "district",
            "password",
            "confirm_password",
        )

    def validate(self, attrs):
        if not any([attrs.get("email", None), attrs.get("phone", None)]):
            raise serializers.ValidationError("Either email or phone is required.")

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Password does not match.")
        return attrs


class UserMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uuid", "first_name", "last_name", "email", "phone")


class UserVerificationSerializer(serializers.Serializer):
    user_uuid = serializers.CharField()
    photo = serializers.ImageField()


class RichUserSerializer(serializers.ModelSerializer):
    requests = serializers.SerializerMethodField()
    proposals = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "uuid",
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "district",
            "requests",
            "proposals",
            "socials",
        )

    def get_requests(self, user):
        user_requests = user.service_requests.all()
        return ServiceRequestSerializer(user_requests, many=True).data

    def get_proposals(self, user):
        user_proposals = user.services.all()
        return ServiceProposalSerializer(user_proposals, many=True).data
    
    def get_socials(self, user):
        socials = UserSocials.objects.filter(user=user).first()
        if socials:
            return {
                "whatsapp": socials.whatsapp,
                "telegram": socials.telegram,
            }
        
        return None
