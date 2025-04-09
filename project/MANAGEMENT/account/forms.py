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


class TeacherLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


