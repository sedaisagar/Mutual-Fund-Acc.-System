from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from utils.common_model import CommonModel
from .manager import CustomUserManager
from utils.enums import ROLE_CHOICES


class User(CommonModel, AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email Address",
        unique=True,
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default="U",
        max_length=1,
    )
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.role == "A"

    @property
    def is_superuser(self):
        return self.role == "A"
