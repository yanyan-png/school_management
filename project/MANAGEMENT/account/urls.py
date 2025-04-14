# URL paths of views under account app

from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/student/', views.student_login_view, name='student_login'),
    path('login/teacher/', views.teacher_login_view, name='teacher_login'),
    path('dashboard/student/', views.student_dashboard_view, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('logout/', views.logout_view, name='logout'),

]
