from rest_framework import serializers

from reviews.models import User


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'token',
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'username', 'email'
        model = User


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.SlugRelatedField(slug_field='username',
    #                                         read_only=True)
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
