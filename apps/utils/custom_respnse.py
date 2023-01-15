from typing import Union

from django.http import JsonResponse
from rest_framework import status


class CustomResponse(JsonResponse):
    def __init__(self,
                 *,
                 data: Union[str, dict] = None,
                 message: Union[str, None] = None,
                 error: Union[str, None] = None,
                 status: int = status.HTTP_200_OK,
                 **kwargs):
        super(CustomResponse, self).__init__(data={"data": data,
                                                   "message": message,
                                                   "error": error, },
                                             status=status,
                                             **kwargs)
