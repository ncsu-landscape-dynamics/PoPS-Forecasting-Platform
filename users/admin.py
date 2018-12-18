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
    fieldsets = UserAdmin.fieldsets + (
            (('User info'), {'fields': ('organization','user_type','email_confirmed')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
            (None, {'fields': ('email','first_name','last_name','organization','user_type','email_confirmed','is_active','is_staff','is_superuser',)}),
    )
    list_display = ['username', 'email','first_name','last_name','organization','email_confirmed','is_staff']

admin.site.register(CustomUser, CustomUserAdmin)