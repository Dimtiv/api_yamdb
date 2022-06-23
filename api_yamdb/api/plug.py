# TODO удалить файл целиком
from reviews.models import User, ROLE_MODERATOR


def setFakeUserToRequest(request):
    # request.user = User.objects.first()
    request.user = User.objects.get(pk=2)
    # request.user.role = ROLE_MODERATOR
