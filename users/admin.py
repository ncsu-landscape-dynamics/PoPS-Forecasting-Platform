# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email','first_name','last_name','organization','email_confirmed']
    fieldsets = (
        (('User'), {'fields': ('username', 'email','first_name','last_name','organization','email_confirmed')}),
        (('Permissions'), {'fields': ('is_active','is_staff','is_superuser')}),
        )

admin.site.register(CustomUser, CustomUserAdmin)
