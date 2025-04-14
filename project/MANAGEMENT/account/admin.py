# account/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import User, Student, Teacher

# ------------------------------
# Custom User Creation Form
# ------------------------------
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'role')

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords don't match.")
        return pw2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# ------------------------------
# Custom User Change Form
# ------------------------------
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'role', 'is_active', 'is_superuser')

# ------------------------------
# Inline Models
# ------------------------------
class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False

class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False

# ------------------------------
# Custom User Admin
# ------------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'first_name', 'last_name', 'role', 'is_superuser')
    list_filter = ('role', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        if obj.role == 'Student':
            return [StudentInline(self.model, self.admin_site)]
        elif obj.role == 'Teacher':
            return [TeacherInline(self.model, self.admin_site)]
        return []

# ------------------------------
# Fallback registration
# ------------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lrn', 'level', 'section', 'parent_name')
    search_fields = ('lrn', 'user__first_name', 'user__last_name')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'department')
    search_fields = ('license_number', 'user__username', 'user__first_name')
