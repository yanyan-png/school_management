from django.shortcuts import render, redirect
from .forms import ClassForm
from django.contrib.auth.decorators import login_required
from account.models import Teacher, Student
from classroom.models import Badge
from django.http import JsonResponse
from .models import Attendance
import json


@login_required
def create_class(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.teacher = teacher
            new_class.save()
            return redirect('account:teacher_dashboard_view')
    else:
        form = ClassForm()

    return render(request, 'teacher/create_class.html', {'form': form})


@login_required
def student_calendar(request):
    try:
        student = Student.objects.get(user=request.user)
        attendances = Attendance.objects.filter(student=student).order_by('-date')
    except Student.DoesNotExist:
        attendances = []

    return render(request, 'student/student_calendar.html', {
        'attendances': attendances,
    })


@login_required
def student_merit_view(request):
    try:
        student = Student.objects.get(user=request.user)
        badges = Badge.objects.filter(student=student, type='merit')
    except Student.DoesNotExist:
        badges = []

    return render(request, 'student/student_merit.html', {'badges': badges})


# ─── NEW: JSON endpoint for FullCalendar ────────────────────────────────
@login_required
def attendance_events(request):
    try:
        student = Student.objects.get(user=request.user)
        attendance_records = Attendance.objects.filter(student=student)
    except Student.DoesNotExist:
        attendance_records = []

    events = []
    for rec in attendance_records:
        # pick a color per status
        if rec.status == 'present':
            color = '#4caf50'   # green
        elif rec.status == 'absent':
            color = '#f44336'   # red
        elif rec.status == 'excused':
            color = '#ff9800'   # orange
        else:
            color = '#2196f3'   # fallback blue

        events.append({
            'title': f"{rec.class_obj.class_name} – {rec.status.capitalize()}",
            'start': rec.date.strftime('%Y-%m-%d'),
            'allDay': True,
            'color': color,
        })

    return JsonResponse(events, safe=False)

def student_announcement(request):
    # You can pass any context you need to the template
    # For example, if you have a model Announcement, fetch all:
    # announcements = Announcement.objects.all()
    # return render(request, 'student/student_announcement.html', {'announcements': announcements})
    
    return render(request, 'student/student_announcement.html')

from .models import Grade
@login_required
def student_starplot(request):
    student_obj = Student.objects.get(user=request.user)

    grades = Grade.objects.filter(student=student_obj)
    radar_chart_data = {}

    for grade in grades:
        subject_name = str(grade.class_obj)  # ensure __str__ method is meaningful
        written = grade.written_work or 0
        performance = grade.performance_task or 0
        final = grade.final_exam or 0
        total = written + performance + final
        radar_chart_data[subject_name] = total

    categories = list(radar_chart_data.keys())
    scores = list(radar_chart_data.values())

    return render(request, 'student/student_starplot.html', {
        'categories': json.dumps(categories),
        'scores': json.dumps(scores),
    })
