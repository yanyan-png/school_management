from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import StudentLoginForm, TeacherLoginForm
from .models import Student, Teacher
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
import logging
from classroom.models import *

# Responsible for the log-in page viewing and validation of Student accounts
def student_login_view(request):
    if request.user.is_authenticated:
        return redirect('account:student_dashboard')  # redirect if already logged in

    form = StudentLoginForm(request.POST or None)
    if form.is_valid():
        lrn = form.cleaned_data['lrn']
        student = Student.objects.get(lrn=lrn)
        user = student.user
        login(request, user)
        return redirect('account:student_dashboard')
    return render(request, 'student/student_login.html', {'form': form})


logger = logging.getLogger(__name__)

# Responsible for the log-in page viewing and validation of Teacher accounts
def teacher_login_view(request):
    if request.user.is_authenticated:
        return redirect('account:teacher_dashboard')

    form = TeacherLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        print(f"Trying to authenticate user: {username}")  # Debug line
        user = authenticate(request, username=username, password=password)

        if user:
            print(f"Authenticated: {user} with role {user.role}")  # Debug line

        if user is not None and user.role.lower() == 'teacher':
            login(request, user)
            print("Login successful!")  # Debug line
            return redirect('account:teacher_dashboard')
        else:
            print("Invalid credentials or role.")  # Debug line
            messages.error(request, "Invalid credentials or not a teacher")

    return render(request, 'teacher/teacher_login.html', {'form': form})



# Responsible for displaying the dashboard of Student accounts
@login_required
def student_dashboard_view(request):
    return render(request, 'student/student_dashboard.html')


# Responsible for displaying the dashboard of Teacher accounts
from classroom.models import Class  # Don't forget to import the model

# classroom/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def teacher_dashboard_view(request):
    teacher = request.user.teacher  # Fetch the teacher object (assuming 1-to-1 relation)
    classes = Class.objects.filter(teacher=teacher)

    # Fetch the enrolled students for each class (you can modify this based on how you want it structured)
    for class_obj in classes:
        class_obj.enrolled_students = class_obj.enrollment_set.all()  # You can fetch the students in this way

    return render(request, 'teacher/teacher_dashboard.html', {'classes': classes})





# Responsible for log-out process
def logout_view(request):
    logout(request)
    return redirect('account:student_login')  # or redirect based on role if needed

