from django.shortcuts import render, redirect
from .models import Class
from .forms import ClassForm
from django.contrib.auth.decorators import login_required
from account.models import Teacher
from django.shortcuts import get_object_or_404

@login_required
def teacher_class_list(request):
    teacher = request.user.teacher  # Assuming 1-to-1 relation
    classes = Class.objects.filter(teacher=teacher)
    return render(request, 'teacher/class_list.html', {'classes': classes})

@login_required


def create_class_view(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.teacher = teacher
            new_class.save()
            form.save_m2m()
            return redirect('account:teacher_dashboard')

    else:
        form = ClassForm()

    return render(request, 'teacher/create_class.html', {'form': form})

# classroom/views.py

from django.shortcuts import render, get_object_or_404
from .models import Class

@login_required
def class_detail_view(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id, teacher__user=request.user)
    return render(request, 'teacher/class_detail.html', {'class': class_obj})


