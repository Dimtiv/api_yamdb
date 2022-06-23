from django.urls import path, include
from rest_framework import routers

from .views import SignUpViewSet, TokenViewSet, ReviewViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('auth/signup', SignUpViewSet, basename='signups')
router.register('auth/token', TokenViewSet, basename='tokens')

router.register(
    r'titles/(?P<title_id>\d+?)/reviews',
    ReviewViewSet,
    'reviews'
)

urlpatterns = [
    path('', include(router.urls)),
]
