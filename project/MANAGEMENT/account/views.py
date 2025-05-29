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
from classroom.models import Attendance
from account.models import Student
from datetime import date
from classroom.models import Badge  # adjust the path if it's in another app





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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date
from .models import Student, Announcement
from classroom.models import Attendance, Grade, Badge
from django.http import JsonResponse


import json

from datetime import date
import json

@login_required
def student_dashboard(request):
    student_obj = Student.objects.get(user=request.user)

    # Attendance
    attendance_qs = Attendance.objects.filter(student=student_obj)
    attendance_data = {
        str(record.date): {
            'status': record.status,
            'time_in': str(record.time_in),
            'time_out': str(record.time_out),
        }
        for record in attendance_qs
    }

    # Badges
    badges = Badge.objects.filter(student=student_obj).order_by('-timestamp')

    # Grades for Radar Plot
    grades = Grade.objects.filter(student=student_obj)
    radar_chart_data = {}

    for grade in grades:
        subject_name = str(grade.class_obj)  # Use __str__ method of Class
        written = grade.written_work or 0
        performance = grade.performance_task or 0
        final = grade.final_exam or 0
        total = written + performance + final
        radar_chart_data[subject_name] = total

    categories = list(radar_chart_data.keys())
    scores = list(radar_chart_data.values())

    # Announcements
    announcements = Announcement.objects.order_by('-date_posted')[:10]

    # ✅ Combine everything into ONE context dict
    context = {
        'attendance_data': attendance_data,
        'badges': badges,
        'today': date.today(),
        'categories': json.dumps(categories),
        'scores': json.dumps(scores),
        'announcements': announcements,  # <-- Don't forget this!
    }

    return render(request, 'student/student_dashboard.html', context)


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

# In account/views.py
def student_merit_view(request):
    # your logic here
    return render(request, 'student/student_merit.html')



from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def qr_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lrn = data.get('lrn')
            student = Student.objects.get(lrn=lrn)
            login(request, student.user)
            return JsonResponse({'success': True, 'redirect_url': '/student/dashboard/'})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid QR code'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

