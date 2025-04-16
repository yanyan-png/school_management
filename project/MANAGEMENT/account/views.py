from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentLoginForm, TeacherLoginForm
from .models import Student, User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from classroom.models import Class
from account.models import Teacher 
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


logger = logging.getLogger(__name__)

def student_login(request):
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


def teacher_login(request):
    if request.user.is_authenticated:
        return redirect('account:teacher_dashboard')  # redirect if already logged in

    form = TeacherLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role.lower() == 'teacher': # Ensure the user is a teacher
            login(request, user)
            return redirect('account:teacher_dashboard')
        else:
            messages.error(request, "Invalid credentials or not a teacher")

    return render(request, 'teacher/teacher_login.html', {'form': form})


@login_required
def student_dashboard(request):
    return render (request, 'student/student_dashboard.html')


@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    classes = Class.objects.filter(teacher=teacher)
    
    return render(request, 'teacher/teacher_dashboard.html', {
        'classes': classes
    })

def logout_view(request):
    logout(request)
    return redirect('account:student_login')  # or redirect based on role if needed