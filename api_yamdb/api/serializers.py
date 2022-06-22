from rest_framework import serializers

from reviews.models import User


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'username', 'confirmation_code'
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'username', 'email'
        model = User


