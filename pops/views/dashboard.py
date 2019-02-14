from django.views.generic import ListView, DetailView, TemplateView, CreateView, View
from ..models import *


class WorkspaceView(TemplateView):
    template_name = 'pops/dashboard/workspace.html'


    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(WorkspaceView, self).get_context_data(**kwargs)
            current_user=self.request.user
            context['current_user']=current_user
            context['user_case_studies'] = CaseStudy.objects.prefetch_related('host_set','pest_set__pest_information').filter(created_by = current_user).order_by('-date_created')[:5]
            context['user_sessions'] = Session.objects.prefetch_related('created_by','case_study').filter(created_by = current_user).order_by('-date_created')
            return context

class DashboardView(TemplateView):
    template_name = 'pops/dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(DashboardView, self).get_context_data(**kwargs)
            try:
                session = Session.objects.get(pk=self.kwargs.get('pk'))
            except:
                session = None
            context['session'] = session
            return context

