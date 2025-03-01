from django.urls import path
from . import views

app_name = 'message'

urlpatterns = [
    path('student_announcement/', views.student_announcement, name='student_announcement'),
]