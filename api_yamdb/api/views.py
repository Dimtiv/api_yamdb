import uuid

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Review, Title, Comment, Genre, Category
from users.models import User, USERNAME_ME

from .utils import Email
from .filters import TitleFilter
from .permissions import IsModerator, IsAdmin, IsOwner, IsReadOnly, IsMe
from .serializers import (
    SignUpSerializer, TokenSerializer, UserSerializer, CommentSerializer,
    GenreSerializer, CategorySerializer, TitleSerializer, ReviewSerializer,
    TitlePostSerializer, MeUserSerializer
)


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(**serializer.validated_data)
        generated_code = str(uuid.uuid4())
        user.confirmation_code = generated_code
        user.save()
        Email.send_email(user.email,
                         f'Ваш код подтверждения: {generated_code}')
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=self.request.data['username'])
        if user.confirmation_code != confirmation_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user).access_token
        return Response(data={'token': str(token)})


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [IsAdmin | IsMe]

    def get_object(self):
        if self.kwargs.get('username') == USERNAME_ME:
            return self.request.user
        return super().get_object()

    def get_serializer_class(self):
        if self.kwargs.get('username') == USERNAME_ME:
            return MeUserSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == USERNAME_ME:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, args, kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReadOnly | IsOwner | IsModerator | IsAdmin]

    def get_queryset(self):
        return Review.objects.filter(title_id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsReadOnly | IsOwner | IsModerator | IsAdmin]

    def get_queryset(self):
        return Comment.objects.filter(
            review_id=self.kwargs.get('review_id')
        )

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsReadOnly | IsAdmin]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsReadOnly | IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializer
        return TitlePostSerializer
