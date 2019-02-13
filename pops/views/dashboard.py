from django.views.generic import ListView, DetailView, TemplateView, CreateView, View
from ..models import *


class WorkspaceView(TemplateView):
    model = CaseStudy
    template_name = 'pops/dashboard/workspace.html'


    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(WorkspaceView, self).get_context_data(**kwargs)
            context['user_case_studies'] = CaseStudy.objects.prefetch_related('host_set','pest_set__pest_information').filter(created_by = self.request.user).order_by('-date_created')
            context['user_sessions'] = Session.objects.all()#filter(created_by = self.request.user).order_by('-date_created')
            return context