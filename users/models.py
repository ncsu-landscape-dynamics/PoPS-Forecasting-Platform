# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    organization = models.CharField(max_length=100, null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    USER_CHOICES = (
        ("STUDENT", "Student"),
        ("GOVERNMENT", "Government Employee"),
        ("INDUSTRY", "Industry Employee"),
        ("UNIVERSITY_RESEARCHER", "University Researcher"),
        ("OTHER", "Other"),
    )
    user_type = models.CharField(max_length=30,
                    choices=USER_CHOICES,
                    default="OTHER",)

    def __str__(self):
        return self.username
