# account/forms.py

from django import forms
from .models import Student, User
from django.contrib.auth import authenticate

class StudentLoginForm(forms.Form):
    lrn = forms.CharField(max_length=50)

    def clean_lrn(self):
        lrn = self.cleaned_data.get('lrn')
        if not Student.objects.filter(lrn=lrn).exists():
            raise forms.ValidationError("Invalid LRN")
        return lrn


from django import forms
from django.contrib.auth.models import User

from django import forms
from .models import User

class TeacherLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Invalid username")
        return username
