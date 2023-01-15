from apps.user.models import User


def get_user_id(phone_number: str) -> tuple[str, bool]:
    user_obj, created = User.objects.get_or_create(phone_number=phone_number, is_deleted=False)
    return str(user_obj.id), created


def get_user_obj(user_id: str) -> User:
    return User.objects.filter(pk=user_id, is_deleted=False).first()


def check_user_exists(user_id: str) -> bool:
    return User.objects.filter(id=user_id, is_deleted=False).exists()


def check_phone_number_exists(phone_number: str) -> bool:
    return User.objects.filter(phone_number=phone_number, is_deleted=False).exists()


def get_user_info(user_id: str, values: list[str]) -> dict:
    return User.objects.values(*values).get(pk=user_id)
