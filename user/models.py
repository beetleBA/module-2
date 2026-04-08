from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('role', 'admin')
        return self.create_user(email, password, **kwargs)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
    )
    role = models.CharField(max_length=20, default='user', choices=[(
        'user', 'Обычный пользователь'), ('admin', 'Администратор')])
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
