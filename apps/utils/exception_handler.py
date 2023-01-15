from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

from apps.utils.custom_respnse import CustomResponse
from apps.utils.exceptions import AuthenticationError
from apps.utils.messages import AUTHORIZATION_ERROR


def base_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, AuthenticationError):
        return CustomResponse(error=AUTHORIZATION_ERROR, status=status.HTTP_401_UNAUTHORIZED)
    if isinstance(exc, ValidationError):
        if isinstance(exc.detail, dict):
            message = ""
            for details in exc.detail.values():
                for error in details:
                    message += str(error) + " "
        else:
            message = " ".join(str(detail) for detail in exc.detail)
        return CustomResponse(error=message,
                              status=status.HTTP_400_BAD_REQUEST)
    return response
