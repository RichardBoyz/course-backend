import jwt, datetime
from rest_framework import exceptions, authentication
from users.models import User


class AppAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")

        if not token:
            raise exceptions.AuthenticationFailed("No token provided")

        token = token.split(" ")[1]

        user_id = decode_access_token(token=token)

        try:
            user = User.objects.get(id=user_id)
        except:
            raise exceptions.AuthenticationFailed("No such user")

        return (user, None)


def create_access_token(id):
    return jwt.encode(
        {
            "user_id": id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
            "iat": datetime.datetime.utcnow(),
        },
        "access",
        algorithm="HS256",
    )


def create_refresh_token(id):
    return jwt.encode(
        {
            "user_id": id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow(),
        },
        "refresh",
        algorithm="HS256",
    )


def decode_access_token(token):
    try:
        payload = jwt.decode(token, "access", algorithms="HS256")

        return payload["user_id"]
    except Exception as e:
        raise exceptions.AuthenticationFailed("unauthenticated")


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, "refresh", algorithms="HS256")

        return payload["user_id"]
    except:
        raise exceptions.AuthenticationFailed("unauthenticated")
