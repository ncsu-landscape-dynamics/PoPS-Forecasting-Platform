# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, MassEmail, EmailListEntry

# To be able to edit and add users in the admin site, we have to register the CustomUser model
class CustomUserAdmin(UserAdmin):
        #CustomUserCreationForm and CustomUserChangeForm are defined in users/forms.py
        add_form = CustomUserCreationForm #add new user form
        form = CustomUserChangeForm #edit user form
        model = CustomUser
        # fieldsets indicate the fields that are shown in the "edit" view for a given user object
        fieldsets = UserAdmin.fieldsets + (
                (('User info'), {'fields': ('organization','user_type','email_confirmed')}),
        )
        # add_fieldsets indicate the fields that are shown in the "add" view for a given user object
        add_fieldsets = UserAdmin.add_fieldsets + (
                (None, {'fields': ('email','first_name','last_name','organization','user_type','email_confirmed','is_active','is_staff','is_superuser',)}),
        )
        # list_display indicate the fields that are shown in the "list" view for users
        list_display = ['username', 'email','first_name','last_name','organization','email_confirmed','is_staff']

class MassEmailAdmin(admin.ModelAdmin):
        
        def submit_email(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
                selected_email = obj[0]
                email_list = EmailListEntry.objects.filter(email_confirmed=True)
                subject = selected_email.subject
                print(subject)
                message = selected_email.message
                domain = settings.WEBSITE_URL
                for email_object in email_list:
                        print(email_object)
                        html_message = render_to_string('html_email_templates/standard_email.html',
                                {'subject': subject, 
                                 'message': message, 
                                 'email': email_object.email,
                                 'domain': domain,
                                 'uid': urlsafe_base64_encode(force_bytes(email_object.pk)),
                                 })
                        plain_message = strip_tags(html_message)
                        send_mail(
                                subject,
                                plain_message,
                                "PoPS Model <noreply@popsmodel.org>",
                                [email_object.email],
                                html_message=html_message,
                                fail_silently=False,
                        )
        
        submit_email.short_description = 'Submit Mail'
        submit_email.allow_tags = True

        actions = ['submit_email'] 
        search_fields = ['subject',]
        list_display = ['subject','created']

#Register our CustomUserAdmin for the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MassEmail, MassEmailAdmin)
admin.site.register(EmailListEntry)