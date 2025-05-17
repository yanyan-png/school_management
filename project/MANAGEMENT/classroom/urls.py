# classroom/urls.py
from django.urls import path
from . import views

app_name = 'classroom'

urlpatterns = [
    path('teacher/classes/create/', views.create_class, name='create_class'),
    path('student/calendar/', views.student_calendar, name='student_calendar'),
]
