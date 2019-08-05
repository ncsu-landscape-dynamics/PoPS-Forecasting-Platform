# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# Here we create the forms for creating and changing users. The creation form is used for sign up
# and the admin site. The change form is used for the admin site.

# CustomUserCreationForm is a subclass of UserCreationForm (from django auth forms). By default,
# the django UserCreationForm contains username (required), email, first name, last name, and password.
# In our custom form, we set email, first and last name to be required. We also bring in our
# custom fields from the CustomUser model in the class Meta.
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='A valid email address is required.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    terms_and_services = forms.BooleanField(label='I agree to the Terms and Conditions.', error_messages={'required': 'You must agree to the terms and services to create an account.'})
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email','first_name','last_name','organization','user_type','password1','password2','terms_and_services',)
    
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email','first_name','last_name','organization','user_type',)

