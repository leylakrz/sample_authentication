import random
import string

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from apps.user.authentication import get_login_info, TokenValidator, generate_access_token, TokenType
from apps.user.queries import get_user_id, check_phone_number_exists
from apps.utils.cache_utils import cache_set_otp, cache_get_otp
from apps.utils.custom_respnse import CustomResponse
from apps.utils.messages import WRONG_OTP_CODE, OTP_SENT, INVALID_INPUT_ERROR
from apps.utils.sms_sender.kave_negar import KaveNegar
from apps.utils.validators import mobile_format
from prj.settings import OTP_CODE_LENGTH


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        self.validate_phone_number(phone_number)
        code = request.data.get("code")
        hash_string = request.data.get("hash_string")
        if code:
            if self.check_otp(phone_number, code):
                user_id, created = get_user_id(phone_number)
                data = get_login_info(user_id)
                data["created"] = created
                return CustomResponse(data=data, )
            else:
                return CustomResponse(error=WRONG_OTP_CODE, status=status.HTTP_401_UNAUTHORIZED, )
        else:
            self.set_and_send_otp(phone_number, hash_string)
            return CustomResponse(message=OTP_SENT)

    @staticmethod
    def validate_phone_number(phone_number):
        if mobile_format.match(phone_number):
            return
        raise ValidationError(INVALID_INPUT_ERROR)

    @staticmethod
    def generate_otp_code() -> str:
        return "".join(random.choices(string.digits, k=OTP_CODE_LENGTH))

    def set_and_send_otp(self, user_phone_number: str, hash_string: str) -> None:
        otp_code = self.generate_otp_code()
        cache_set_otp(user_phone_number, otp_code, )
        self.send_login_sms(user_phone_number, otp_code, hash_string)

    @staticmethod
    def check_otp(user_phone_number, received_otp_code) -> bool:
        otp_code = cache_get_otp(user_phone_number)
        return otp_code == received_otp_code

    @staticmethod
    def send_login_sms(phone_number, otp_code, hash_string, ):
        sms_sender = KaveNegar()
        if check_phone_number_exists(phone_number):
            sms_sender.send_login_sms(
                code=otp_code, number=phone_number, hash_str=hash_string)
        else:
            sms_sender.send_signup_sms(
                code=otp_code, number=phone_number, hash_str=hash_string)


class RefreshView(APIView, TokenValidator):
    token_type = TokenType.REFRESH.value

    def post(self, request):
        refresh_token = request.META.get('HTTP_X_REFRESH_TOKEN')
        token_payload = self.get_token_payload(refresh_token)
        self.check_token_type(token_payload)
        user_id = self.get_user_id_from_payload(token_payload)
        return CustomResponse(data={"access_token": generate_access_token(user_id), })
