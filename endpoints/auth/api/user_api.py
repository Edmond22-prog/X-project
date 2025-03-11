import os

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from app_models.models import User, UserVerification
from middlewares.auth_middleware import check_is_connected
from serializers.user_serializer import (
    RegisterUserSerializer,
    RichUserSerializer,
    UserMinSerializer,
    UserVerificationSerializer,
)
from utils.user_utils import get_connected_user


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
            is_active=True,
        )
        user.password = make_password(validated_data["password"])
        user.save()

        return Response(UserMinSerializer(user).data, status=status.HTTP_201_CREATED)


class UserVerificationAPIView(APIView):
    serializer_class = UserVerificationSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_id="verify_user",
        operation_description="Endpoint for user verification",
        operation_summary="Verify an user",
        request_body=UserVerificationSerializer,
        responses={200: "Message"},
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
        try:
            user = User.objects.get(uuid=validated_data["user_uuid"])
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        
        # Save the uploaded image with a specific name
        photo = validated_data["photo"]
        file_extension = os.path.splitext(photo.name)[1]
        new_file_name = f"{user.first_name}-{user.last_name}-vd{file_extension}"
        photo_content = ContentFile(photo.read())
        
        # Check if the user has already uploaded a verification photo
        try:
            user_verif = UserVerification.objects.get(user=user)
            user_verif.verification_photo.delete()
            user_verif.verification_photo.save(new_file_name, photo_content)
            
        except UserVerification.DoesNotExist:
            user_verif = UserVerification.objects.create(
                user=user, verification_photo=new_file_name
            )
            user_verif.verification_photo.save(new_file_name, photo_content)

        return Response(
            {"message": "Picture registered successfully ! Please wait for validation."},
            status=status.HTTP_200_OK,
        )


class ConnectedUserAPIView(APIView):
    @swagger_auto_schema(
        operation_id="connected_user",
        operation_description="Endpoint to get the connected user",
        operation_summary="Get the connected user",
        responses={200: RichUserSerializer()},
        tags=["Users"],
        security=[{"Bearer": []}],
    )
    @check_is_connected
    def get(self, request, *args, **kwargs):
        connected_user = get_connected_user(request)
        if not connected_user:
            return Response(
                {"error": "Connected user not found !"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            RichUserSerializer(connected_user).data, status=status.HTTP_200_OK
        )
