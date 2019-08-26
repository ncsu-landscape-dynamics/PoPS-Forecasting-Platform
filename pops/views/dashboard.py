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
 
    #outputs = Output.objects.filter(run_id = run_id)
    this_run = Run.objects.get(pk=run_id)
    first_year = this_run.run_collection.session.case_study.end_year+1
    run_collection = this_run.run_collection
    steering_year = this_run.steering_year
    print('Steering year:')
    print(steering_year)
    defaults = { 
            'steering_year' : 0,
            'management_cost' : 0,
            'management_area' : 0,	
            'output' : [
            {
                'year': 2019,	
                'number_infected': 1000,
                'infected_area': 15000,
                'escape_probability' : 50,
            },
            {
                'year': 2020,	
                'number_infected': 20000,
                'infected_area': 35000,
                'escape_probability' : 70,
            },	
            {
                'year': 2021,	
                'number_infected': 30000,
                'infected_area': 58000,
                'escape_probability' : 90,
            }
        ]
        }
    steering_outputs = [
        { 
            'steering_year' : 2019,
            'management_cost' : 1000000,
            'management_area' : 2000,	
            'output' : [
            {
                'year': 2019,	
                'number_infected': 1000,
                'infected_area': 10000,
                'escape_probability' : 50,
            },
            {
                'year': 2020,	
                'number_infected': 2000,
                'infected_area': 20000,
                'escape_probability' : 70,
            },	
            {
                'year': 2021,	
                'number_infected': 3000,
                'infected_area': 40000,
                'escape_probability' : 90,
            }
        ]
        },
        { 
            'steering_year' : 2020,
            'management_cost' : 2000000,
            'management_area' : 4000,	
            'output' : [
            {
                'year': 2020,	
                'number_infected': 1800,
                'infected_area': 15000,
                'escape_probability' : 50,
            },	
            {
                'year': 2021,	
                'number_infected': 2500,
                'infected_area': 20000,
                'escape_probability' : 60,
            }
        ]
        },
        { 
            'steering_year' : 2021,
            'management_cost' : 3000000,
            'management_area' : 5000,		
            'output' : [
            {
                'year': 2021,	
                'number_infected': 2200,
                'infected_area': 10000,
                'escape_probability' : 40,
            }
        ]
        }
        ]
    #get all inputs for runs in this collection (management polygons)
    inputs = Run.objects.filter(run_collection=run_collection)
    #get the outputs for this run
    outputs = Output.objects.filter(run_id = run_id) 
    #then merge the outputs for previous runs to get the previous steering years
    if steering_year:
        print('Steering year true')
        steering_boolean=True
        for x in range(first_year, steering_year):
            print(x)
            run = Run.objects.get(run_collection=run_collection, steering_year=x)
            print(run)
            outputs = outputs | Output.objects.filter(run_id=run,year=x)
    else:
        print('Steering year false')
        steering_boolean=False
    print('Data:')
    #print(all_steering_years)
    print(first_year)
    #print(steering_year)
    print(outputs)
    data = {"run_inputs": {
        "primary_key": this_run.pk,
        "date_created":this_run.date_created,
        "status":this_run.status,
        "steering_year":this_run.steering_year,
        "management_cost": this_run.management_cost,
        "management_area": this_run.management_area,
        "management_polygons": this_run.management_polygons,
        },
    "inputs": list(inputs.order_by('steering_year').values("pk","date_created","id","steering_year", "management_cost", "management_polygons", "management_area")),
    "results": list(outputs.order_by('year').values("pk","date_created","id","number_infected", "infected_area", "year", "single_spread_map","probability_map","escape_probability")),
    "all_steering_years": steering_outputs,
    "no_management_default": defaults,
    "steering": steering_boolean
    }
    return JsonResponse(data)

def check_status(request):
    run_id = request.GET.get('new_run_id', None)
    run = Run.objects.get(pk=run_id)
    data = {
        "status":run.status,
        }
    return JsonResponse(data)

def delete_runs(request):
    run_id = request.GET.get('run_id', None)
    run_collection = request.GET.get('run_collection', None)
    runs= Run.objects.filter(run_collection=run_collection, pk__gte=run_id)
    print('Run collection is:' + run_collection)
    print('The run id is:' + run_id)
    print(runs)
    runs.delete()
    data = {
        "run_id":run_id,
        }
    return JsonResponse(data)

class OutputDetailView(DetailView):
    template_name = 'pops/dashboard/detail_output.html'
    model = Output

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


