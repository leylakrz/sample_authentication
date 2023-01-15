# Create your models here.
from django.db import models

from apps.utils.base.base_model import BaseModel


class Gender(models.TextChoices):
    MALE = "M", "مرد"
    FEMALE = "F", "زن"


class User(BaseModel):
    phone_number = models.CharField(max_length=11)
    birth_date = models.DateField(null=True)
    full_name = models.CharField(max_length=300, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, null=True)
