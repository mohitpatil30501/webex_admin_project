import uuid

from django.contrib.auth.models import User
from django.db import models


class CollegeTeacherData(models.Model):
    id = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)


class Teacher(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), unique=True, primary_key=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    college_data = models.ForeignKey(CollegeTeacherData, on_delete=models.CASCADE)
    email_verification = models.BooleanField(default=False)
    password_state = models.BooleanField(default=True)
