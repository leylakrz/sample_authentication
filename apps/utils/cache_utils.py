from django.core.cache import cache

from apps.utils.decorators.decorators import redis_error_handler
from vod_api.settings import OTP_TIMEOUT_SECOND

otp_cache_key = lambda user_phone_number: f"otp_{user_phone_number}"


@redis_error_handler
def cache_set_otp(user_phone_number, otp_code):
    cache.set(otp_cache_key(user_phone_number), otp_code, OTP_TIMEOUT_SECOND)


@redis_error_handler
def cache_get_otp(user_phone_number):
    return cache.get(otp_cache_key(user_phone_number))
