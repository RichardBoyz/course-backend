from .models import Course
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

    def to_internal_value(self, data):
        user = self.context["request"].user

        data["lecturers"] = [user.id]
        data["creator"] = user.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["time_week"] = instance.get_time_week_display()
        return data
