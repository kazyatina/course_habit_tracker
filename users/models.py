from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель Пользователь"""

    username = models.CharField(
        max_length=150, verbose_name="Ник", unique=False, default="User"
    )
    email = models.EmailField(unique=True, verbose_name="Почта")

    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефон"
    )
    avatar = models.ImageField(
        upload_to="media/users/avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город")
    tg_chat_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="chat-id Телеграм"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
