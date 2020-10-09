# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# CustomUser is a model that extends django's default User.
# The default User has username (required), first name, last name, 
# email, and password. By extending the default user, we can add
# additional fields required for our use, but still take advantage
# of Django's built-in authentication system. 


class CustomUser(AbstractUser):

    # user's organization
    organization = models.CharField(max_length=100, null=True, blank=True)
    # email_confirmed is used in the account activation method
    email_confirmed = models.BooleanField(default=False)
    USER_CHOICES = (
        (None, "Select the option that best describes you:"),
        ("STUDENT", "Student"),
        ("GOVERNMENT", "Government Employee"),
        ("INDUSTRY", "Industry Employee"),
        ("UNIVERSITY_RESEARCHER", "University Researcher"),
        ("OTHER", "Other"),
    )
    user_type = models.CharField(max_length=30,
                                 choices=USER_CHOICES,
                                 )

    class Meta(object):
        # Require that email be a unique field in the database
        unique_together = ('email',)

    def __str__(self):
        return self.username


class MassEmail(models.Model):
    subject = models.CharField(max_length=200)
    created = models.DateTimeField(verbose_name="date created", 
                                   auto_now=False, auto_now_add=True)
    message = models.TextField()

    def __unicode__(self):
        return self.subject

    class Meta:
        verbose_name = "Mass Email to all Member"
        verbose_name_plural = "Mass Email"


class EmailListEntry(models.Model):

    email = models.EmailField(blank=False, null=False)

    class Meta(object):
        # Require that email be a unique field in the database
        unique_together = ('email',)

    def __str__(self):
        return self.email