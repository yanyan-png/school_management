from django.contrib import admin
from .models import Class, Enrollment, Attendance, Grade, Badge, Announcement


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'subject', 'teacher')
    search_fields = ('class_name', 'subject')
    list_filter = ('teacher',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj')
    search_fields = ('student__user__username', 'class_obj__class_name')
    list_filter = ('class_obj',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'date', 'status')
    list_filter = ('class_obj', 'status', 'date')
    search_fields = ('student__user__username',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'written_work', 'performance_task', 'final_exam')
    list_filter = ('class_obj',)
    search_fields = ('student__user__username',)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'type', 'shard_count', 'points', 'timestamp')
    list_filter = ('type', 'class_obj')
    search_fields = ('student__user__username',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_obj', 'teacher', 'date_posted')
    search_fields = ('title', 'content')
    list_filter = ('class_obj', 'teacher')
