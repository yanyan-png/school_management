from django.shortcuts import render

def inbox_view(request):
    return render(request, 'message/inbox.html')  # Make sure the template exists
