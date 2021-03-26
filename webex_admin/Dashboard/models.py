import os
import uuid
from db_file_storage.model_utils import delete_file, delete_file_if_needed

from django.db import models
from User.models import *


# Details Page
def profile_pic_file_name(instance, filename):
    extension = ''
    for ch in filename[::-1]:
        extension = ch + extension
        if ch == '.':
            break

    path = "Dashboard.ProfilePicFile/bytes/filename/mimetype"
    file_format = str(instance.id) + "_profile_pic" + extension
    return os.path.join(path, file_format)


class Details(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    id = models.UUIDField(default=uuid.uuid4(), unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=200, blank=True, null=True, default=None)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, blank=True, null=True, default=None)
    mobile = models.CharField(max_length=10, blank=True, null=True, default=None)
    address = models.CharField(max_length=500, blank=True, null=True, default=None)
    date_of_birth = models.CharField(max_length=10, blank=True, null=True, default=None)

    profile_file = models.FileField(upload_to=profile_pic_file_name, blank=True, null=True, default=None)

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'profile_file')
        super(Details, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Details, self).delete(*args, **kwargs)
        delete_file(self, 'profile_file')


class ProfilePicFile(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=200)


# Designation Page
class Designation(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4(), unique=True, primary_key=True)

    designation = models.CharField(max_length=100, blank=True, null=True, default=None)
    department = models.CharField(max_length=100, blank=True, null=True, default=None)
    institute = models.CharField(max_length=200, blank=True, null=True, default=None)
