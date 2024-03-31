from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import UserSerializer, TeacherSerializer
from courses.serializers import GetCourseSerializer
from .filters import UserFilter
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .authentication import (
    create_access_token,
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

        response = Response()

        response.set_cookie(key="jwt", value=access_token, httponly=True)
        response.data = {
            "token": access_token,
            "user_id": user.id,
            "role": user.role,
        }
        return response


class UserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    @action(methods=["GET"], detail=False, url_path="teachers")
    def getTeacher(self, request):
        users = User.objects.filter(role="teacher")
        serializer_data = TeacherSerializer(users, many=True).data
        return Response(serializer_data)


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
