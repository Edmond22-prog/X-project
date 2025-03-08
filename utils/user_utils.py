import logging
import re
from typing import Any

from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings


User = get_user_model()


def get_connected_user(request: Any):
    """
    Get the current user from the request.

    :param request:
    :return:
    """
    header_token = request.META.get("HTTP_AUTHORIZATION", None)
    if not header_token or header_token == "Bearer":
        return None

    token = re.sub("Bearer ", "", header_token)
    if token == "undefined":
        return None

    # # Check if the token is blacklisted
    # if BlacklistedToken.objects.filter(token=token).exists():
    #     logging.warning("Token is blacklisted")
    #     return None

    # Verified the token and retrieve user
    try:
        payload = api_settings.JWT_DECODE_HANDLER(token)
        if payload.get("type") == "refresh":
            # So this is maybe a refresh token
            return None

        existing_username = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER(payload)
    except:
        logging.exception("Error while decoding the token")
        return None

    existing_user = User.objects.get_by_natural_key(existing_username)
    if not existing_user:
        return None

    return existing_user
