from django.urls import path
from . import views

urlpatterns = [
    # Add real views later
    path('', views.inbox_view, name='inbox'),
]
