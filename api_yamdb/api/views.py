from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Review, Title, Comment, Genre, Category
from .emails import Util
from .filters import TitleFilter
from .permissions import (
    IsModerator, IsAdmin, IsOwner, IsReadOnly
)
from .serializers import (
    SignUpSerializer, TokenSerializer, UserSerializer, CommentSerializer,
    GenreSerializer, CategorySerializer, TitleGetSerializer, ReviewSerializer,
    TitlePostSerializer, MeUserSerializer
)
from .tokens import account_activation_token


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        headers = self.get_success_headers(serializer.data)
        user = get_object_or_404(User, username=self.request.data['username'])
        confirmation_code = account_activation_token.make_token(user)
        Util.send_email(self.request.data['email'], confirmation_code)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers)


class TokenViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        confirmation_code = self.request.data['confirmation_code']
        user = get_object_or_404(User, username=self.request.data['username'])
        if user is not None and account_activation_token.check_token(
                user, confirmation_code):
            token = RefreshToken.for_user(user).access_token
            return Response(data={'token': str(token)})


class UserViewSet(ModelViewSet):
    """
    Viewset для получения, создания, редактирования и удаления пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]


class MeUserViewSet(ModelViewSet):
    """
    Viewset для получения и редактирования своего профиля.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_object(self):
        user = User.objects.get(username=self.request.user)
        return user

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def list(self, request):
        # возвращаем 'retrieve' вместо 'list' для прохождения теста.
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        serializer = MeUserSerializer(
            user,
            data=self.request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class CreateListDestroyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                               mixins.DestroyModelMixin, GenericViewSet):
    pass


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsReadOnly | IsAdmin]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleGetSerializer
    permission_classes = [IsReadOnly | IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleGetSerializer
        return TitlePostSerializer
