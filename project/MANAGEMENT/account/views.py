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
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date
from .models import Student
from classroom.models import Attendance, Grade, Badge
from django.http import JsonResponse


import json

from datetime import date




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
from django.shortcuts import render, get_object_or_404
from datetime import date
import json
from classroom.models import Attendance, Badge, Grade, Class, Enrollment, Announcement
from account.models import Student


@login_required
def student_dashboard(request):
    student_obj = get_object_or_404(Student, user=request.user)

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
        subject_name = str(grade.class_obj)
        written = grade.written_work or 0
        performance = grade.performance_task or 0
        final = grade.final_exam or 0
        total = written + performance + final
        radar_chart_data[subject_name] = total

    categories = list(radar_chart_data.keys())
    scores = list(radar_chart_data.values())

    # ✅ Announcements: only for student's enrolled classes
    enrolled_classes = Class.objects.filter(enrollments__student=student_obj)
    announcements = Announcement.objects.filter(class_obj__in=enrolled_classes).select_related('class_obj').order_by('-date_posted')

    context = {
        'attendance_data': attendance_data,
        'badges': badges,
        'today': date.today(),
        'categories': json.dumps(categories),
        'scores': json.dumps(scores),
        'announcements': announcements,  # Use original queryset here
    }

    return render(request, 'student/student_dashboard.html', context)



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from classroom.models import Class, Badge, Announcement
from account.models import Teacher

from django.db.models import Prefetch
from classroom.models import Enrollment
from account.models import Student  # Ensure Student has a OneToOneField to User

from django.db.models import Prefetch
from classroom.models import Enrollment, Badge, Class, Announcement
from account.models import Student, Teacher

@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    classes = Class.objects.filter(teacher=teacher).prefetch_related(
        Prefetch('enrollments', queryset=Enrollment.objects.select_related('student__user'))
    )

    announcements = Announcement.objects.all().order_by('-date_posted')[:5]

    # FIXED LINE:
    badges = Badge.objects.filter(class_obj__teacher=teacher).select_related('student__user')

    return render(request, 'teacher/teacher_dashboard.html', {
        'classes': classes,
        'announcements': announcements,
        'badges': badges,
    })




def logout_view(request):
    logout(request)
    return redirect('account:student_login')  # or redirect based on role if needed



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