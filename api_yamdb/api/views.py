from django.shortcuts import get_object_or_404
from rest_framework import mixins, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User, Review, Title, Comment, Genre, Category
from .emails import Util
from .permissions import (IsModerator, IsAdmin, IsOwner, IsReadOnly)
from .serializers import (
    SignUpSerializer, TokenSerializer, UserSerializer, CommentSerializer,
    GenreSerializer, CategorySerializer, TitleSerializer, ReviewSerializer
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    def get_object(self):
        username = self.kwargs.get('username')
        if username == 'me':
            return self.request.user
        return super().get_object()


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
    serializer_class = TitleSerializer
    permission_classes = [IsReadOnly | IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__name', 'category__name')
