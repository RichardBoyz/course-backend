from .models import Course
from rest_framework import serializers
from users.models import User


class BaseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class GetCourseSerializer(BaseCourseSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["time_week"] = instance.get_time_week_display()
        return data


class CreateCourseSerializer(BaseCourseSerializer):
    student = serializers.SlugRelatedField(
        slug_field="id", queryset=User.objects.all(), many=True, required=False
    )

    def to_internal_value(self, data):
        user = self.context["request"].user

        data["lecturers"] = [user.id]
        data["creator"] = user.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["time_week"] = instance.get_time_week_display()
        return data
