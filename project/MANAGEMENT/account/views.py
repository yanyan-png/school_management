from django.shortcuts import render
from django.shortcuts import render
from classroom.models import Badge, Grade, Attendance
#from django.contrib.auth.decorators import login_required


def student_dashboard(request):
    return render(request, 'student/student_dashboard.html')


def login(request):
    return render(request, 'login.html')

