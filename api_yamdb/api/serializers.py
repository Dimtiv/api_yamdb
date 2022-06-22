from rest_framework import serializers

from reviews.models import Genre, Title, Category, User


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'username', 'confirmation_code'
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'username', 'email'
        model = User
