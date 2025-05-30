# classroom/urls.py
from django.urls import path
from . import views

app_name = 'classroom'

urlpatterns = [
    path('teacher/classes/create/', views.create_class, name='create_class'),
    path('student/calendar/', views.student_calendar, name='student_calendar'),
    path('student/merit/', views.student_merit_view, name='student_merit'),
    path('student-announcement/', views.student_announcement, name='student_announcement'),
    path('student_starplot/', views.student_starplot, name='student_starplot'),
    path('teacher/class/', views.teacher_class, name='teacher_class'),
    
    path('calendar/', views.teacher_calendar, name='teacher_calendar'),

]
