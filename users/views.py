from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.authentication import get_authorization_header
from .serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .authentication import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
)

from .models import User

# import jwt, datetime


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key="jwt", value=access_token, httponly=True)
        response.data = {"token": access_token}
        return response


class UserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refreshToken")

        id = decode_refresh_token(refresh_token)

        access_token = create_access_token(id)

        return Response({"token": access_token})


class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(key="jwt")
        response.data = {"message": "success"}
        return response
