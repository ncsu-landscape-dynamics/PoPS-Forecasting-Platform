import datetime
from django import forms
from .models import Question, Topic

class SubmitFAQForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['topic', 'question_text', 'answer']