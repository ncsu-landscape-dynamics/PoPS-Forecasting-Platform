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
        
        def submit_email(self,request, obj, email_list): #`obj` is queryset, so there we only use first selection, exacly obj[0]
                selected_email = obj[0]
                email_uidb64 = urlsafe_base64_encode(force_bytes(selected_email.pk))
                subject = selected_email.subject
                print(subject)
                message = selected_email.message
                domain = settings.WEBSITE_URL
                for email_address in email_list:
                        print(email_address)
                        user_uid = urlsafe_base64_encode(force_bytes(email_address.pk))
                        html_message = render_to_string('html_email_templates/standard_email.html',
                                {'subject': subject, 
                                 'message': message, 
                                 'email': email_address.email,
                                 'domain': domain,
                                 'uid': user_uid,
                                 'email_uidb64': email_uidb64,
                                 })
                        plain_message = (subject + '\r\n \r\n' + strip_tags(message) + '\r\n \r\n'
                                        + 'View email as webpage: ' + domain 
                                        + '/accounts/email/' + str(email_uidb64) + '/ \r\n'
                                        + 'Unsubscribe: ' + domain 
                                        + '/accounts/email_list/unsubscribe/' + str(user_uid) + '/')
                        print(plain_message)
                        send_mail(
                                subject,
                                plain_message,
                                "PoPS Model <noreply@popsmodel.org>",
                                [email_address.email],
                                html_message=html_message,
                                fail_silently=False,
                        )
                        return None

        def send_all(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
                print('Send all')
                email_list = EmailListEntry.objects.filter(email_confirmed=True)
                self.submit_email(request, obj, email_list)
                return None

        def test_send(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
                print('Test send')
                email_list = EmailListEntry.objects.filter(email_confirmed=True, receive_test_emails=True)
                self.submit_email(request, obj, email_list)
                return None

        send_all.short_description = 'Send Mass Email'
        send_all.allow_tags = True
        test_send.short_description = 'Send Test (to admins)'
        test_send.allow_tags = True

        actions = ['test_send','send_all'] 
        search_fields = ['subject',]
        list_display = ['subject','created']

#Register our CustomUserAdmin for the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MassEmail, MassEmailAdmin)
admin.site.register(EmailListEntry)