# classroom/urls.py
from django.urls import path
from . import views

app_name = 'classroom'

urlpatterns = [
    path('teacher/classes/create/', views.create_class, name='create_class'),
    # Add other URL patterns here...
]
