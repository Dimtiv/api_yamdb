from django.contrib import admin

from .models import Review, Comment, Genre, Category, Title, User

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
