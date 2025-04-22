from django.db import models
from account.models import Teacher, Student
from django.utils.timezone import now


class Class(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'absent'),
        ('excused', 'excused'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField(null=True, blank=True)
    time_out = models. TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    written_work = models.FloatField()
    performance_task = models.FloatField()
    final_exam = models.FloatField()
    final_grade = models.FloatField()


class Badge(models.Model):
    MERIT = 'merit'
    DEMERIT = 'demerit'
    
    TYPE_CHOICES = [
        (MERIT, 'Merit'),
        (DEMERIT, 'Demerit'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    shard_count = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(default=now)

    def add_shard(self):
        """Adds a shard, converts it to points if the limit is reached."""
        if self.type == self.MERIT:
            shard_limit = 5  # 5 shards for a merit badge
        else:
            shard_limit = 4  # 4 shards for a demerit badge
        
        self.shard_count += 1
        
        if self.shard_count >= shard_limit:
            self.points += 1  # Convert to a full badge
            self.shard_count = 0  # Reset shards

        self.save()

    def __str__(self):
        return f"{self.student} - {self.type} ({self.points} points, {self.shard_count} shards)"

