# account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import StudentLoginForm, TeacherLoginForm
from .models import Student, Teacher
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

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

import logging

logger = logging.getLogger(__name__)

def teacher_login_view(request):
    if request.user.is_authenticated:
        return redirect('account:teacher_dashboard')

    form = TeacherLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        logger.info(f"Attempting login for user: {username}")  # Log the username attempt
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == 'Teacher':  
            logger.info(f"User {username} authenticated successfully.")  # Log successful authentication
            login(request, user)
            return redirect('account:teacher_dashboard')
        else:
            logger.warning(f"Invalid credentials for user: {username}")  # Log failed authentication
            messages.error(request, "Invalid credentials or not a teacher")

    return render(request, 'teacher/teacher_login.html', {'form': form})






@login_required
def student_dashboard_view(request):
    return render(request, 'student/student_dashboard.html')

@login_required
def teacher_dashboard_view(request):
    return render(request, 'teacher/teacher_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('account:student_login')  # or redirect based on role if needed

