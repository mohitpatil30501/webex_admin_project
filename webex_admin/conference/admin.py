from django.contrib import admin

from .models import *


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'last_modification')


@admin.register(StudentData)
class StudentDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


@admin.register(TeacherData)
class StudentDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
