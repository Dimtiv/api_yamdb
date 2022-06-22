from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .emails import Util
from .serializers import SignUpSerializer, TokenSerializer


class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        headers = self.get_success_headers(serializer.data)
        user = get_object_or_404(User, username=self.request.data['username'])
        token = RefreshToken.for_user(user).access_token
        Util.send_email(self.request.data['email'], token)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
