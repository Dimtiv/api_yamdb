from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Genre, Title, Category, User, Review, Comment, \
    ROLE_ADMIN


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = 'token',
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    # username = serializers.SlugRelatedField(read_only=True, slug_field='username')
    # email = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        fields = 'username', 'email'
        model = User
        # read_only_fields = ('username', 'email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def update(self, instance, validated_data):
        validation_fields = [
            'username',
            'email'
        ]
        for field in validation_fields:
            if not validated_data.get(field):
                raise serializers.ValidationError(f'{field} is required')
        if self.context['request'].user.role != ROLE_ADMIN:
            validated_data.pop('role')
        return super(UserSerializer, self).update(instance, validated_data)


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    genre = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        return Review.objects.aggregate(rating=Avg('score'))
