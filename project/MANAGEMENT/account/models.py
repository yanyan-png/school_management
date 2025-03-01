from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions', blank=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lrn = models.CharField(max_length=50, unique=True)
    level = models.CharField(max_length=10)
    section = models.CharField(max_length=50)
    parent_name = models.CharField(max_length=255)
    parent_email = models.EmailField()
    parent_contact = models.CharField(max_length=20)
    photo = models.TextField()

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=255)
    photo = models.TextField()
