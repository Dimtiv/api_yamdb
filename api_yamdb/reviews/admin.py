from django.contrib import admin

from users.models import User
from .models import Review, Comment, Genre, Category, Title

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
