from django.shortcuts import render

from django.views.generic.list import ListView

from .models import Member

class MemberListView(ListView):

    model = Member
    template_name = 'team.html'
    context_object_name = 'members'
