# classroom/models.py

from django.db import models
from account.models import Student, Teacher

class Class(models.Model):
    class_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_name} - {self.subject}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'classroom')

    def __str__(self):
        return f"{self.student} enrolled in {self.classroom}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('excused', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)
    written_work = models.FloatField()
    performance_task = models.FloatField()
    final_exam = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.classroom}"


class Badge(models.Model):
    TYPE_CHOICES = [
        ('merit', 'Merit'),
        ('demerit', 'Demerit'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    shard_count = models.IntegerField()
    points = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.title()} - {self.student} - {self.classroom}"
