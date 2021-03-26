import uuid

from django.contrib.auth.models import User
from django.db import models


class AccessToken(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    last_modification = models.DateTimeField(auto_now_add=True)


class ClassRoom(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), unique=True, primary_key=True)
    title = models.TextField(blank=True, null=True)
    cisco_id = models.TextField(blank=True, null=True)
    room_id = models.TextField(blank=True, null=True)
    meeting_id = models.TextField(blank=True, null=True)
    meeting_number = models.CharField(max_length=50, blank=True, null=True)


class StudentData(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    class_year = models.IntegerField()
    section = models.CharField(max_length=10)
    roll_no = models.IntegerField()
    cisco_id = models.TextField(blank=True, null=True)
    display_name = models.TextField(blank=True, null=True)


class TeacherData(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    cisco_id = models.TextField()
