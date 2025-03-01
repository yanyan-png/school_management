from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

def student_dashboard(request):
    return render(request, 'student/student_dashboard.html')

def student_announcement(request):
    return render(request, 'student/student_announcement.html')

