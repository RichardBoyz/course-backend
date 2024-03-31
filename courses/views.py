from rest_framework.viewsets import ModelViewSet
from .models import Course
from .serializers import (
    BaseCourseSerializer,
    GetCourseSerializer,
    CreateCourseSerializer,
)
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from users.serializers import UserSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = BaseCourseSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCourseSerializer
        if self.action == "list" or self.action == "retrieve":
            return GetCourseSerializer
        return super().get_serializer_class()

    @action(methods=["GET"], detail=True, url_path="students")
    def get_students(self, request, pk):
        course = Course.objects.get(pk=pk)
        if not course:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(
            UserSerializer(course.student.all(), many=True).data,
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.creator.id != request.user.id:
            Response(status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.creator.id != request.user.id:
            Response(status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
