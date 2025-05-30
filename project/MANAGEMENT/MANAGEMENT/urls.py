# project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),  # default app
    path('classroom/', include(('classroom.urls', 'classroom'), namespace='classroom')),  # classroom app with namespace
    path('message/', include('message.urls')),
    # Remove the duplicate entries:
    # path('account/', include('account.urls')),
    # path('account/', include(('account.urls', 'teacher'), namespace='teacher')),
    # path('classroom/', include('classroom.urls')),
]
