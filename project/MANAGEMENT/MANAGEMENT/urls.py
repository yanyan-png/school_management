"""
URL configuration for MANAGEMENT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# school_management/urls.py (or your project root urls.py)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),  # 👈 include the account app URLs
    path('classroom/', include('classroom.urls')),
    path('admin/', admin.site.urls),
    path('classroom/', include('classroom.urls')),  # ✅ Make sure this line exists
    path('account/', include('account.urls')),
    path('message/', include('message.urls')),
    path('api/', include('classroom.urls')),
    
]

