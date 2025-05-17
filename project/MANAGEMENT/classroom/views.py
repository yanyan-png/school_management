# classroom/views.py
from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import ClassForm
from django.contrib.auth.decorators import login_required
from account.models import Teacher

@login_required
def create_class(request):
    # Get the teacher object based on the logged-in user
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.teacher = teacher  # Set the teacher for this class
            new_class.save()
            return redirect('account:teacher_dashboard_view')  # Redirect to the dashboard after creating the class
    else:
        form = ClassForm()

    return render(request, 'teacher/create_class.html', {'form': form})

@login_required
def student_calendar(request):
    return render(request, 'student/student_calendar.html')
