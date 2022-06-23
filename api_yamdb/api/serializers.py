from rest_framework import serializers

from reviews.models import User, Genre, Category


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = 'token',
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'username', 'email'
        model = User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
