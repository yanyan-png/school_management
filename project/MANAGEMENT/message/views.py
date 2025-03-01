from django.shortcuts import render


def student_announcement(request):
    return render(request, 'student/student_announcement.html')
