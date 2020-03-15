# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, MassEmail

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
                selected = obj[0]
                users = CustomUser.objects.filter(is_active=True).filter(email_confirmed=True)
                for user in users:
                        user.email_user(selected.subject, selected.message)
                #EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
        
        submit_email.short_description = 'Submit Mail'
        submit_email.allow_tags = True

        actions = [ 'submit_email' ]
        search_fields = ['subject',]
        list_display = ['subject', 'created']

#Register our CustomUserAdmin for the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MassEmail, MassEmailAdmin)