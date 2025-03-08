from rest_framework import serializers

from app_models.models import User


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
        if not any([attrs["email"], attrs["phone"]]):
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
