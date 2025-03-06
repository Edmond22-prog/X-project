import logging

import jwt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken

from serializers.auth_serializer import LoginSerializer, RefreshSerializer


class LoginAPIView(ObtainJSONWebToken):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_id="login",
        operation_description="Endpoint for user authentication",
        operation_summary="Login an user",
        request_body=LoginSerializer,
        responses={200: "Token and Refresh token"},
        tags=["Auth"],
        security=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors["non_field_errors"][0]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Access all data in the POST request
        token_data = super(LoginAPIView, self).post(request, *args, **kwargs).data
        try:
            user_data = jwt.decode(token_data["token"], verify=False)
        except Exception as e:
            logging.exception(e)
            return Response(
                {"error": "Authentication fails"}, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh_token = api_settings.JWT_ENCODE_HANDLER(
            {
                "user_email": user_data["email"],
                "user_phone": user_data["phone"],
                "orig_iat": user_data["orig_iat"],
                "type": "refresh",
            }
        )

        return Response(
            {"token": token_data["token"], "refresh": refresh_token},
            status=status.HTTP_200_OK,
        )


class RefreshAPIView(RefreshJSONWebToken):
    serializer_class = RefreshSerializer

    @swagger_auto_schema(
        operation_id="refresh",
        operation_description="Endpoint for token refresh",
        operation_summary="Refresh a token",
        request_body=RefreshSerializer,
        responses={200: "Token and Refresh token"},
        tags=["Auth"],
        security=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors["non_field_errors"][0]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Access all data in the POST request
        token_data = super(RefreshAPIView, self).post(request, *args, **kwargs).data
        try:
            user_data = jwt.decode(token_data["token"], verify=False)
        except Exception as e:
            logging.exception(e)
            return Response(
                {"error": "Refresh token fails"}, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh_token = api_settings.JWT_ENCODE_HANDLER(
            {
                "user_email": user_data["email"],
                "user_phone": user_data["phone"],
                "orig_iat": user_data["orig_iat"],
                "type": "refresh",
            }
        )

        return Response(
            {"token": token_data["token"], "refresh": refresh_token},
            status=status.HTTP_200_OK,
        )
