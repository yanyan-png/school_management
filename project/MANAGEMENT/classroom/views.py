from django.shortcuts import render, redirect
from .forms import ClassForm
from django.contrib.auth.decorators import login_required
from account.models import Teacher, Student
from classroom.models import Badge  # Make sure Badge is imported from your classroom app

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
    return render(request, 'student/student_calendar.html')

@login_required
def student_merit_view(request):
    try:
        student = Student.objects.get(user=request.user)
        badges = Badge.objects.filter(student=student, type='merit')  # Only merit badges
    except Student.DoesNotExist:
        badges = []

    return render(request, 'student/student_merit.html', {'badges': badges})
