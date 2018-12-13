# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='A valid email address is required.')
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email','first_name','last_name','organization','user_type',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','organization')
