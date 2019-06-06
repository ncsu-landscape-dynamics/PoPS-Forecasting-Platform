from django.views.generic import FormView, ListView, DetailView, TemplateView, CreateView, View
from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..models import *
from ..forms import *

 
class NewSessionView(CreateView):
    template_name = 'pops/dashboard/new_session.html'
    form_class = SessionForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        # obj = form.instance or self.object
        return reverse("dashboard", kwargs={'pk': self.object.pk})

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
    template_name = 'pops/dashboard/APHIS_June2019.html'

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(DashboardView, self).get_context_data(**kwargs)
            try:
                session = Session.objects.get(pk=self.kwargs.get('pk'))
            except:
                session = None
            context['session'] = session
            return context
            

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
                'session': self.kwargs.get('pk')
            }
            return JsonResponse(data)
        else:
            return response
 
class AJAXTestView(AjaxableResponseMixin, CreateView):
    template_name = 'pops/dashboard/APHIS_June2019.html'
    form_class = RunForm
    success_url = 'new_session'

    def get_initial(self):
            # call super if needed
            return {'session': self.kwargs.get('pk')}

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(AJAXTestView, self).get_context_data(**kwargs)
            try:
                session = Session.objects.get(pk=self.kwargs.get('pk'))
            except:
                session = None
            try:
                runs = Run.objects.prefetch_related('output_set').filter(session__pk=self.kwargs.get('pk')).filter(status='SUCCESS').order_by('-date_created')

            except:
                runs = None                

            context['session'] = session
            context['runs'] = runs
            return context

def get_output_view(request):
    run_id = request.GET.get('new_run_id', None)
 
    outputs = Output.objects.filter(run_id = run_id)
    run = Run.objects.get(pk=run_id)
    data = {"run_inputs": {
        "name": run.name, 
        "primary_key": run.pk,
        "description": run.description,
        "date_created":run.date_created,
        "status":run.status,
        "random_seed": run.random_seed,
        "reproductive_rate": run.reproductive_rate,
        "distance_scale": run.distance_scale,
        "weather": run.weather,
        "budget": run.budget,
        "cost_per_hectare": run.cost_per_hectare,
        "efficacy": run.efficacy,
        "final_year": run.final_year,
        "management_polygons": run.management_polygons,
        },
    "results": list(outputs.values("date_created","id","number_infected", "infected_area", "years", "spread_map"))
    }
    return JsonResponse(data)

def check_status(request):
    run_id = request.GET.get('new_run_id', None)
    run = Run.objects.get(pk=run_id)
    data = {
        "status":run.status,
        }
    return JsonResponse(data)