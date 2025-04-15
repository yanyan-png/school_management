# account/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentLoginForm, TeacherLoginForm
from .models import Student, User

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
from django.contrib.auth import authenticate, login
from django.contrib import messages

logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import TeacherLoginForm
from django.contrib import messages

def teacher_login_view(request):
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



# account/views.py

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def student_dashboard_view(request):
    return render (request, 'student/student_dashboard.html')

@login_required
def teacher_dashboard_view(request):
   return render (request, 'teacher/teacher_dashboard.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('account:student_login')  # or redirect based on role if needed


