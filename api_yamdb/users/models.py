from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_ADMIN = 'admin'
ROLE_MODERATOR = 'moderator'
ROLE_USER = 'user'
ROLES = (
    (ROLE_ADMIN, 'Администратор'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_USER, 'Пользователь')
)
USERNAME_ME = 'me'


class User(AbstractUser):
    username = models.CharField(
        'Логин', max_length=150, unique=True)
    email = models.EmailField(
        'Почта', max_length=254, unique=True)
    role = models.CharField(
        'Роль', choices=ROLES, default=ROLE_USER, max_length=15)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    first_name = models.CharField(
        'Имя', max_length=150, blank=True)
    last_name = models.CharField(
        'Фамилия', max_length=150, blank=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return bool(self.role == ROLE_ADMIN or self.is_staff)
