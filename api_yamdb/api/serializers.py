from rest_framework import serializers

from reviews.models import User


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = 'token',
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'username', 'email'
        model = User

