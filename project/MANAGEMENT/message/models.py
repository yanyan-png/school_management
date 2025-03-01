from django.db import models
from classroom.models import Class
from account.models import Teacher, Student


class Announcement(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class AnnouncementPhoto(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    photo_path = models.TextField()

class Feedback(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('resolved', 'Resolved'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    timestamp = models.DateTimeField(auto_now_add=True)


