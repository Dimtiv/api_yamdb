from django.shortcuts import get_object_or_404
from rest_framework import mixins, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User, Review, Title, Comment, Genre, Category, \
    ROLE_ADMIN
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .emails import Util
from .permissions import (
    IsModerator, IsAdmin, IsOwner, IsReadOnly, ForUserViewSetIsAdmin, ForUserViewSetIsOwner, IsAdminOrSelf
)
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
    # permission_classes = [IsAdminOrSelf]

    def get_object(self):
        username = self.kwargs.get('username')
        if username == 'me':
            # self.permission_classes = [IsAuthenticated]
            print('set permission')
            return self.request.user
        # print(self.action)
        # self.permission_classes = [ForUserViewSetIsAdmin]
        return super().get_object()

    @action(detail=True, methods='patch')
    def me(self, request):
        print('ME function')
        self.permission_classes = [IsAdminOrSelf]
        user = self.get_object()
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def get_permissions(self):
        print(f'The action is: {self.action.upper()}')
        # methods = ['list', 'create', 'destroy']
        if self.action == ['partial_update', 'retrieve']:
            permission_classes = [IsAdminOrSelf]
        else:
            permission_classes = [ForUserViewSetIsAdmin]
        return [permission() for permission in permission_classes]

    # def perform_update(self, serializer):
    #     # self.permission_classes = [ForUserViewSetIsAdmin]
    #     serializer.save()

    # @action(methods='patch', detail=False, permission_classes=[IsOwner, IsAdmin])
    # def update(self, request, *args, **kwargs):
    #     super(UserViewSet, self).update(self.request.data)

    # def get_permissions(self):
    #     username = self.kwargs.get('username')
    #     if username == 'me':
    #         self.check_object_permissions(self.request.user, self.get_object().user)

    # def list(self, request, *args, **kwargs):
    #     self.permission_classes = IsAdminOnly
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # @action(detail=False, permission_classes=IsAdmin)
    # def get_queryset(self):
    #     # serializer = UserSerializer(self.request.user)
    #     if self.request.user.is_authenticated and self.request.user.role == ROLE_ADMIN:
    #         # return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
    #         return User.objects.all()
        # queryset = self.filter_queryset(self.get_queryset())
        # serializer = self.get_serializer(queryset, many=True)
        # raise HttpResponseForbidden
        # return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        # raise HttpResponseForbidden
        # raise status.HTTP_403_FORBIDDEN("You're don't have permissions for this!")


    # def get_object(self):
    #     username = self.kwargs.get('username')
    #     if username == 'me':
    #         return self.request.user
    #     return super().get_object()

    # def check_object_permissions(self, request, obj):
    #     for permission in self.get_permissions():
    #         if not permission.has_object_permission(request, self, obj):
    #             self.permission_denied(
    #                 request,
    #                 message=getattr(permission, 'message', None),
    #                 code=getattr(permission, 'code', None)
    #             )


class MeUserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated)
    http_method_names = ['get', 'patch']

    def list(self, request, *args, **kwargs):
        queryset = User.objects.filter(username=self.request.user)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pass

    def get_queryset(self):
        print(__name__)
        return User.objects.filter(username=self.request.user)


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsReadOnly | IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__name', 'category__name')
