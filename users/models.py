from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        TEACHER = "teacher", "老師"
        STUDENT = "student", "學生"

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=7, choices=Role.choices, default=Role.STUDENT)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
