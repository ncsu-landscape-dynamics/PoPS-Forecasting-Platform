from django.shortcuts import render

from django.views.generic.list import ListView

from .models import Member

class MemberListView(ListView):

    model = Member
    template_name = 'team.html'
    context_object_name = 'members'

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(MemberListView, self).get_context_data(**kwargs)
            members=self.get_queryset()
            context['current_members'] = members.filter(category = "CURRENT").order_by('rank')
            context['past_members'] = members.filter(category = "PAST").order_by('rank')
            context['affiliate_members'] = members.filter(category = "AFFILIATE").order_by('rank')
            return context