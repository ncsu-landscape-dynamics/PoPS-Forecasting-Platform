from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import Question, Topic
from .forms import SubmitFAQForm

def faq_list(request):
    faqs = Question.objects.filter(status=1).order_by('topic__sort_order','topic','sort_order')
    return render(request, 'faq_list.html', {'faqs':faqs})
