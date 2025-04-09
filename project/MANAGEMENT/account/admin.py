# account/admin.py

from django.contrib import admin
from .models import User, Student, Teacher

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'is_superuser')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lrn', 'level', 'section', 'parent_name')
    search_fields = ('lrn', 'user__first_name', 'user__last_name')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'department')
    search_fields = ('license_number', 'user__username', 'user__first_name')
