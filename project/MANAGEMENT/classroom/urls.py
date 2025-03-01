from django.urls import path
from . import views

app_name = 'classroom'

urlpatterns = [
    path('student_calendar/', views.student_calendar, name='student_calendar'),
    path('student_starplot/', views.student_starplot, name='student_starplot'),
    path('student_merit/', views.student_merit, name='student_merit'),
]