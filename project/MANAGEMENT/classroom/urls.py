from django.urls import path
from . import views

app_name = 'classroom'

urlpatterns = [
    path('teacher/classes/', views.teacher_class_list, name='teacher_classes'),
    path('teacher/classes/create/', views.create_class_view, name='create_class'),
]
