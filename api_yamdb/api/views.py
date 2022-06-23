from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Review, Title
from .emails import Util
from .permissions import OwnerOrReadOnly, IsModerator, IsAdmin
from .plug import setFakeUserToRequest
from .serializers import SignUpSerializer, TokenSerializer, ReviewSerializer


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        headers = self.get_success_headers(serializer.data)
        user = get_object_or_404(User, username=self.request.data['username'])
        token = RefreshToken.for_user(user).access_token
        Util.send_email(self.request.data['email'], token)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class TokenViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        confirmation_code = self.request.data['confirmation_code']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        headers = self.get_success_headers(serializer.data)
        user = get_object_or_404(User, username=self.request.data['username'])
        token = RefreshToken.for_user(user).access_token
        Util.send_email(self.request.data['email'], token)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [OwnerOrReadOnly | IsModerator | IsAdmin]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        # TODO убрать заглушку
        setFakeUserToRequest(self.request)
        serializer.save(author=self.request.user, title=title)
