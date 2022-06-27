from django.urls import path, include
from rest_framework import routers

from .views import SignUpViewSet, TokenViewSet, UserViewSet
from .views import SignUpViewSet, TokenViewSet, ReviewViewSet, CommentViewSet
from .views import SignUpViewSet, TokenViewSet, ReviewViewSet, CommentViewSet, GenreViewSet, CategoryViewSet, TitleViewSet, MeUserViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register('auth/signup', SignUpViewSet, basename='signups')
router.register('auth/token', TokenViewSet, basename='tokens')
router.register('users/me', MeUserViewSet, basename='single_user')
router.register('users', UserViewSet, basename='users')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'titles', TitleViewSet, basename='titles')


router.register(
    r'titles/(?P<title_id>\d+?)/reviews',
    ReviewViewSet,
    'reviews'
)
router.register(
    r'titles/(?P<title_id>\d+?)/reviews/(?P<review_id>\d+?)/comments',
    CommentViewSet,
    'comments'
)

urlpatterns = [
    path('', include(router.urls)),
]
