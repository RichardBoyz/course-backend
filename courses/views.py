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

    @action(methods=["GET"], detail=False, url_path="enrolled-courses")
    def get_enrolled_courses(self, request):
        course = Course.objects.filter(student=request.user.id)

        serializer = GetCourseSerializer(course, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["DELETE"], detail=True, url_path="cancel-course")
    def cancel_course(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)

            if request.user in course.student.all():
                course.student.remove(request.user)
                course.save()
                return Response(
                    {"message": "Course cancelled successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "You are not enrolled in this course"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(methods=["GET"], detail=False, url_path="my-courses")
    def get_my_courses(self, request):
        course = Course.objects.filter(creator=request.user.id)

        serializer = GetCourseSerializer(course, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True, url_path="students")
    def get_course_students(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)

            students = course.student.all()
            serializer = UserSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND
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
