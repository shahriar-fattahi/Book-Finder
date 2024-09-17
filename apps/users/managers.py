from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(
        self,
        username: str,
        password: str,
        **extra_fields,
    ):
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            username=username,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str,
        password: str,
        **extra_fields,
    ):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            username=username,
            password=password,
            **extra_fields,
        )

    def create_superuser(
        self,
        username: str,
        password: str,
        **extra_fields,
    ):
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(
            username=username,
            password=password,
            **extra_fields,
        )
