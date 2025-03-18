from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона", blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name="Страна", blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", verbose_name="Аватар", blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["email"]
        permissions = [
            ("can_view_users", "can view users"),
            ("can_block_users", "can block users"),
        ]

    def __str__(self):
        return self.email
