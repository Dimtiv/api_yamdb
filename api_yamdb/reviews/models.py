from django.contrib.auth.models import AbstractUser
from django.db import models


# class User(AbstractUser):
#     pass

class Review(models.Model):
    text = models.TextField()


    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Comment(models.Model):
    pass

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Genre(models.Model):
    pass

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Category(models.Model):
    pass

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tile(models.Model):
    pass

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    pass

    class Meta:
        verbose_name = 'Жанр Произведения'
        verbose_name_plural = 'Жанры произведений'

