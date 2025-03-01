from django.shortcuts import render

def student_calendar(request):
    return render(request, 'student/student_calendar.html')

def student_starplot(request):
    return render(request, 'student/student_starplot.html')

def student_merit(request):
    return render(request, 'student/student_merit.html')