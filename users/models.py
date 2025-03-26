from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель сотрудника."""
    username = models.CharField(max_length=128,
                                unique=True,
                                verbose_name="Имя сотрудника",
                                help_text="Введите ваше имя.")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
