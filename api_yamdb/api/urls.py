from django.urls import path, include
from rest_framework import routers

from .views import SignUpViewSet, TokenViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('auth/signup', SignUpViewSet, basename='signups')
router.register('auth/token', TokenViewSet, basename='tokens')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
]
