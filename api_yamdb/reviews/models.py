from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

ROLE_ADMIN = 'admin'
ROLE_MODERATOR = 'moderator'
ROLE_USER = 'user'
ROLES = (
    (ROLE_ADMIN, 'Администратор'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_USER, 'Пользователь')
)


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


class Genre(models.Model):
    # name = models.CharField(max_length=256)
    # slug = models.SlugField(max_length=50, unique=True)
    #
    # def __str__(self):
    #     return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(models.Model):
    # name = models.CharField(max_length=256)
    # slug = models.SlugField(max_length=50, unique=True)
    #
    # def __str__(self):
    #     return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    # name = models.CharField()
    # year = models.PositiveIntegerField(
    #     validators=[MaxValueValidator(datetime.now().year)],
    #     )
    # description = models.CharField(blank=True, null=True)
    # genre = models.ManyToManyField(Genre, through='GenreTitle')
    # category = models.ForeignKey(
    #     Category,
    #     models.SET_NULL,
    #     related_name='titles',
    #
    # )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    # genre = models.ForeignKey(Genre, on_delete=models.CASCADE())
    # title = models.ForeignKey(Title, on_delete=models.CASCADE())
    #
    # def __str__(self):
    #     return f'{self.title} {self.genre}'

    class Meta:
        verbose_name = 'Жанр Произведения'
        verbose_name_plural = 'Жанры произведений'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_title_author')
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']
