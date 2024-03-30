from django.db import models
from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_courses"
    )
    student = models.ManyToManyField(User, related_name="enrolled_courses")
    lecturers = models.ManyToManyField(User, related_name="teach_courses")

    class TimeWeek(models.IntegerChoices):
        MONDAY = 1, "每周一"
        TUESDAY = 2, "每周二"
        WEDNESDAY = 3, "每周三"
        THURSDAY = 4, "每周四"
        FRIDAY = 5, "每周五"
        SATURDAY = 6, "每周六"
        SUNDAY = 7, "每周日"

    time_week = models.IntegerField(choices=TimeWeek.choices)
    time_period = models.CharField(max_length=255)
