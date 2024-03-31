from rest_framework import serializers
from .models import User
from courses.serializers import GetCourseSerializer


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "role", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class UserSerializer(BaseUserSerializer):

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class TeacherSerializer(BaseUserSerializer):

    def to_representation(self, instance):
        result = super().to_representation(instance)
        lecturer_courses = instance.teach_courses.all()
        serializer_data = GetCourseSerializer(lecturer_courses, many=True).data
        result["teach_courses"] = serializer_data
        return result
