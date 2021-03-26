from django.contrib import admin
from .models import *


@admin.register(CollegeTeacherData)
class CollegeTeacherDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher',)
