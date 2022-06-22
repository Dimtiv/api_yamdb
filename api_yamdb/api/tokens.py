import jwt
from django.conf import settings


def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token
