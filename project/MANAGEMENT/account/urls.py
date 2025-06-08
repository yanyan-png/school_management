# account/urls.py

from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    path('login/student/', views.student_login, name='student_login'),
    path('login/teacher/', views.teacher_login, name='teacher_login'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('classroom/', include('classroom.urls')),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/qr-login/', views.qr_login, name='qr_login'),  # NEW
    path('student/merit/', views.student_merit, name='student_merit'),
    

]
