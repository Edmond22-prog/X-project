from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_models.models import User
from serializers.user_serializer import RegisterUserSerializer, UserMinSerializer


class RegisterUserAPIView(APIView):
    serializer_class = RegisterUserSerializer

    @swagger_auto_schema(
        operation_id="register_user",
        operation_description="Endpoint for user registration",
        operation_summary="Register an user",
        request_body=RegisterUserSerializer,
        responses={201: UserMinSerializer()},
        tags=["Users"],
        security=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors["non_field_errors"][0]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data.get("email", None),
            phone=validated_data.get("phone", None),
            city=validated_data.get("city", None),
            district=validated_data.get("district", None),
        )
        user.password = make_password(validated_data["password"])
        user.save()

        return Response(UserMinSerializer(user).data, status=status.HTTP_201_CREATED)
