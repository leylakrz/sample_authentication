from typing import Callable

import redis

from vod_api.settings import logger


def redis_error_handler(func: Callable) -> Callable:
    """
    a decorator for handling redis errors
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (redis.exceptions.ConnectionError, redis.exceptions.ResponseError) as error:
            logger.error(f"cache_manager.{func.__name__} {type(error)}: {str(error)}")
            # return f"{type(error)}: {str(error)}"

    return wrapper


def general_error_handler(func: Callable) -> Callable:
    """
    a decorator for handling errors
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            logger.error(f"{type(error)}: {str(error)}")

    return wrapper
