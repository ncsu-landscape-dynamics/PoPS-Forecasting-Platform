from django.views.generic import FormView, ListView, DetailView, TemplateView, CreateView, View
from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from django.db.models import Prefetch

from ..models import *
from ..forms import *

class SessionAjaxableResponseMixin:
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
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        session_id=self.object.pk
        new_run_collection = RunCollection(session=self.object,name='Default',default=True)
        new_run_collection.save()
        new_run=Run(run_collection=new_run_collection)
        new_run.save()
        session=self.object
        session.default_run=new_run
        session.save()
        if self.request.is_ajax():
            data = {
                'session_pk': self.object.pk,
                'run_collection_pk': new_run_collection.pk,
                'run_pk': new_run.pk,
                'case_study_pk': self.object.case_study.pk,
            }
            return JsonResponse(data)
        else:
            return response
 
class NewSessionView(SessionAjaxableResponseMixin, CreateView):
    template_name = 'pops/dashboard/new_session.html'
    form_class = SessionForm


    def get_success_url(self, **kwargs):
        # obj = form.instance or self.object
        return reverse("dashboard", kwargs={'pk': self.object.pk})

""" class NewSessionView(CreateView):
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
 """
class WorkspaceView(TemplateView):
    template_name = 'pops/dashboard/workspace.html'

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(WorkspaceView, self).get_context_data(**kwargs)
            current_user=self.request.user
            context['current_user']=current_user
            context['user_case_studies'] = CaseStudy.objects.prefetch_related('host_set','pest_set__pest_information').filter(created_by = current_user).order_by('-date_created')[:5]
            context['user_sessions'] = Session.objects.prefetch_related('created_by','case_study').filter(created_by = current_user).order_by('-date_created')[:5]
            context['number_of_sessions'] = Session.objects.filter(created_by = current_user).count()
            return context

class SessionListView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    #paginate_by = 5  # if pagination is desired
    template_name = 'pops/dashboard/session_list.html'

    def get_queryset(self):
        return Session.objects.prefetch_related('run_set','created_by','case_study').filter(created_by = self.request.user).order_by('-date_created')

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(SessionListView, self).get_context_data(**kwargs)
            context['sessions']=self.get_queryset()
            return context

    # def get_queryset(self):
    #     return CaseStudy.objects.filter(Q(staff_approved = True ) | Q(created_by = self.request.user))

class DashboardTempView(TemplateView):
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
                'name': self.object.name,
                'description': self.object.description,
                'status': self.object.status,
                'random_seed': self.object.random_seed,
                'date_created': self.object.date_created,
                'budget': self.object.budget,
                'efficacy': self.object.efficacy,
                'tangible_landscape': self.object.tangible_landscape,
                'cost_per_meter_squared': self.object.cost_per_meter_squared,
            }
            return JsonResponse(data)
        else:
            return response
 
class DashboardView(AjaxableResponseMixin, CreateView):
    template_name = 'pops/dashboard/dashboard.html'
    form_class = RunCollectionForm
    success_url = 'new_session'

    def get_initial(self):
            # call super if needed
            return {'session': self.kwargs.get('pk')}

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(DashboardView, self).get_context_data(**kwargs)
            try:                
                session = Session.objects.get(pk=self.kwargs.get('pk'))
            except:
                session = None
            #Get case study pk    
            case_study = session.case_study

            #try:
            #    runs = Run.objects.filter(session__pk=self.kwargs.get('pk')).filter(status='SUCCESS').order_by('-date_created').prefetch_related(Prefetch('output_set', queryset=Output.objects.defer('spread_map').order_by('years')))
            #except:
            #    runs = None   
            try:
                historic_data = HistoricData.objects.filter(case_study=case_study).order_by('year')
            except:
                historic_data = None   
            try:
                mapbox_parameters = MapBoxParameters.objects.get(case_study=case_study)
            except:
                historic_data = None   
                
            print(session)
            print(case_study)
            print(mapbox_parameters)
            steering_years = range(case_study.end_year +1, session.final_year+1)
            context['session'] = session
            context['case_study'] = case_study
            context['mapbox_parameters'] = mapbox_parameters
            #context['runs'] = runs
            context['historic_data'] = historic_data
            print(historic_data)
            context['steering_years'] = steering_years
            return context

@method_decorator(csrf_exempt, name='post')
class NewRunView(CreateView):
    template_name = 'pops/dashboard/dashboard.html'
    form_class = RunForm
    success_url = 'new_session'

    def post(self, request, *args, **kwargs):
        run_form = self.form_class(request.POST)
        if run_form.is_valid():
            new_run = run_form.save()
            if self.request.is_ajax():
                data = {
                    'pk': new_run.pk,
                    'steering_year': new_run.steering_year,
                }
                return JsonResponse(data)
            else:
                return self.render_to_response(
                    self.get_context_data(
                    success=True
                )
        )
        else:
            if self.request.is_ajax():
                return JsonResponse(run_form.errors, status=400)
            else:
                return self.render_to_response(
                self.get_context_data(
                        answer_form=answer_form,
                        question_form=question_form
                )
        )
    

@method_decorator(ensure_csrf_cookie, name='get')
class DashboardTestView(AjaxableResponseMixin, CreateView):
    template_name = 'pops/dashboard/dashboard_test.html'
    form_class = RunForm
    success_url = 'new_session'

    def get_initial(self):
            # call super if needed
            return {'session': self.kwargs.get('pk')}

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(DashboardTestView, self).get_context_data(**kwargs)
            try:
                session = Session.objects.get(pk=self.kwargs.get('pk'))
            except:
                session = None
            try:
                runs = Run.objects.filter(session__pk=self.kwargs.get('pk')).filter(status='SUCCESS').order_by('-date_created').prefetch_related(Prefetch('output_set', queryset=Output.objects.defer('spread_map').order_by('years')))

            except:
                runs = None                

            context['session'] = session
            context['runs'] = runs
            context['historic_data'] = ['2014','2015','2016','2017','2018']
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
        "cost_per_meter_squared": run.cost_per_meter_squared,
        "management_month": run.management_month,
        "management_cost": run.management_cost,
        "management_area": run.management_area,
        "efficacy": run.efficacy,
        "final_year": run.final_year,
        "management_polygons": run.management_polygons,
        },
    "results": list(outputs.order_by('years').values("pk","date_created","id","number_infected", "infected_area", "years", "spread_map"))
    }
    return JsonResponse(data)

def check_status(request):
    run_id = request.GET.get('new_run_id', None)
    run = Run.objects.get(pk=run_id)
    data = {
        "status":run.status,
        }
    return JsonResponse(data)

class OutputDetailView(DetailView):
    template_name = 'pops/dashboard/detail_output.html'
    model = Output

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


