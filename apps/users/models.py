from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    def __str__(self) -> str:
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
