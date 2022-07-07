import uuid

from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import Email
from reviews.models import Genre, Title, Category, Review, Comment
from users.models import User, USERNAME_ME


class SignInSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def save(self, **kwargs):
        return str(
            RefreshToken.for_user(self.validated_data['user']).access_token
        )

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        if user.confirmation_code != attrs['confirmation_code']:
            raise ValidationError(
                {'detail': 'Неверный код!'})
        attrs['user'] = user
        return attrs


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        fields = ('username', 'email')
        model = User

    @staticmethod
    def validate_username(value):
        if value == USERNAME_ME:
            raise serializers.ValidationError(
                f"Username не может принимать значение '{USERNAME_ME}'. "
                f"Данное значение зарезервировано!")
        return value

    def validate(self, attrs):
        if User.objects.filter(
                email=attrs['email']).first() != User.objects.filter(
                username=attrs['username']).first():
            raise ValidationError(
                {'detail': 'Данный email или username уже используются!'})
        return attrs

    def save(self, **kwargs):
        user, created = User.objects.get_or_create(**self.validated_data)
        generated_code = str(uuid.uuid4())
        user.confirmation_code = generated_code
        user.save()
        Email.send_email(user.email,
                         f'Ваш код подтверждения: {generated_code}')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User


class MeUserSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class CurrentTitleIdDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs.get('title_id')

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    title_id = serializers.HiddenField(
        default=CurrentTitleIdDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title_id')
        model = Review
        read_only_fields = ('author', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title_id'),
                message='Вы уже оставляли отзыв для данного произведения!'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        read_only_fields = ('rating', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        return Title.objects.filter(id=obj.id).aggregate(
            rating=Round(Avg('reviews__score'))).get('rating')


class TitlePostSerializer(TitleSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
