from django.contrib import admin

from .models import *
from .forms import UserChoiceField
from User.models import Teacher


@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'id', 'name',)
    readonly_fields = ('id',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            return UserChoiceField(queryset=Teacher.objects.filter())

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProfilePicFile)
class ProfilePicFileAdmin(admin.ModelAdmin):
    pass

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            return UserChoiceField(queryset=Teacher.objects.filter())

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'id',)
    readonly_fields = ('id',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            return UserChoiceField(queryset=Teacher.objects.filter())

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
