from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, TemplateView, CreateView, View
from django.contrib.auth.decorators import login_required
from rest_framework import serializers
from django.forms import ModelForm, modelform_factory
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden

from ..models import *
from ..forms import *

class CaseStudyReview(DetailView):

    model = CaseStudy
    template_name = 'pops/case_study_review2.html'

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(CaseStudyReview, self).get_context_data(**kwargs)
            #casestudy = CaseStudy.objects.select_related('weather').get(pk=self.kwargs.get('pk')) #get_object_or_404(CaseStudy, pk=pk)
            hosts = Host.objects.filter(case_study__pk=self.kwargs.get('pk'))
            pests = Pest.objects.filter(case_study__pk=self.kwargs.get('pk')).select_related('pest_information')
            # Create any data and add it to the context
            #context['casestudy'] = casestudy
            context['hosts'] = hosts
            context['pests'] = pests
            return context

class NewCaseStudyView(TemplateView):

    template_name = 'pops/create_case_study2.html'
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
             permission = self.check_permissions(request, pk=pk)
             if not permission:
                 return HttpResponseForbidden()
        my_forms, database_content=self.initialize_forms(request, pk=pk)
        required_models, success, optional_models = self.validate_forms(my_forms)
        if success:
            required_models = self.save_forms(request, required_models, success, optional_models)
            return redirect('case_study_review2', pk=required_models['new_case_study'].pk)
        else:
            my_forms['error_message'] = "Please correct the errors below:"    
        context ={**my_forms, **database_content}
        return self.render_to_response(context) 

    def check_permissions(self, request, pk):
        cs = get_object_or_404(CaseStudy, pk=pk)
        if cs.created_by == request.user:
            return True
        return

    def initialize_forms(self, request, pk=None):
        my_forms={}
        original_datafiles={}
        post_data = request.POST or None
        file_data = request.FILES or None
        cs=None
        host=None
        mortality=None
        pest=None
        vector=None
        weather=None
        wind=None
        seasonality=None
        lethal_temp=None
        temperature=None
        precipitation=None
        temperature_polynomial=None
        precipitation_polynomial=None
        temperature_reclass=None
        precipitation_reclass=None
        if pk:
            cs = get_object_or_404(CaseStudy, pk=pk)
            original_datafiles['infestation_data'] = cs.infestation_data
            original_datafiles['all_plants_data'] = cs.all_plants
            original_datafiles['treatment_data'] = cs.treatment_data
            host = get_object_or_404(Host, case_study=cs)
            original_datafiles['host_data'] = host.host_data
            mortality = Mortality.objects.get_or_none(host=host)   
            if mortality:
                original_datafiles['mortality_data'] = mortality.mortality_data
            pest = get_object_or_404(Pest, case_study=cs)
            vector = Vector.objects.get_or_none(pest=pest)
            if vector:
                original_datafiles['vector_data'] = vector.vector_data
            weather = get_object_or_404(Weather, case_study=cs)
            wind = Wind.objects.get_or_none(weather=weather)
            seasonality = Seasonality.objects.get_or_none(weather=weather)
            lethal_temp = LethalTemperature.objects.get_or_none(weather=weather)
            temperature = Temperature.objects.get_or_none(weather=weather)
            precipitation = Precipitation.objects.get_or_none(weather=weather)
            temperature_polynomial = TemperaturePolynomial.objects.get_or_none(temperature=temperature)
            precipitation_polynomial = PrecipitationPolynomial.objects.get_or_none(precipitation=precipitation)
            temperature_reclass=TemperatureReclass.objects.filter(temperature=temperature)
            precipitation_reclass=PrecipitationReclass.objects.filter(precipitation=precipitation)
        my_forms['case_study_form'] = CaseStudyForm(post_data, file_data, instance=cs, prefix='cs')
        my_forms['host_form'] = HostForm(post_data, file_data, instance=host, prefix='host')
        my_forms['mortality_form'] = MortalityForm(post_data, file_data, instance=mortality, prefix='mortality')
        my_forms['pest_form'] = PestForm(post_data, file_data, instance=pest, prefix='pest')
        my_forms['vector_form'] = VectorForm(post_data, file_data, instance=vector, prefix='vector')
        my_forms['weather_form'] = WeatherForm(post_data, instance=weather, prefix='weather')
        my_forms['wind_form'] = WindForm(post_data, instance=wind, prefix='wind')
        my_forms['seasonality_form'] = SeasonalityForm(post_data, instance=seasonality, prefix='seasonality')
        my_forms['lethal_temp_form'] = LethalTemperatureForm(post_data, instance=lethal_temp, prefix='lethal_temp')
        my_forms['temperature_form'] = TemperatureForm(post_data, instance=temperature, prefix='temperature')
        my_forms['precipitation_form'] = PrecipitationForm(post_data, instance=precipitation, prefix='precipitation')
        my_forms['temperature_polynomial_form'] = TemperaturePolynomialForm(post_data, instance=temperature_polynomial, prefix='temperature_polynomial')
        my_forms['precipitation_polynomial_form'] = PrecipitationPolynomialForm(post_data, instance=precipitation_polynomial, prefix='precipitation_polynomial')
        TemperatureReclassFormSet = forms.inlineformset_factory(Temperature, TemperatureReclass, form=TemperatureReclassForm, min_num=2, validate_min=True, extra=1)
        my_forms['temperature_reclass_formset'] = TemperatureReclassFormSet(post_data, instance=temperature, prefix='temp_reclass')
        PrecipitationReclassFormSet = forms.inlineformset_factory(Precipitation, PrecipitationReclass, form=PrecipitationReclassForm, min_num=2, validate_min=True, extra=1)
        my_forms['precipitation_reclass_formset'] = PrecipitationReclassFormSet(post_data, instance=precipitation, prefix='precip_reclass')
        return my_forms, original_datafiles

    def validate_forms(self, my_forms):
        required_models={}
        optional_models={}
        optional_models['new_case_study']=[]
        optional_models['host']=[]
        optional_models['pest']=[]
        optional_models['weather']=[]
        optional_models['temperature']=[]
        optional_models['precipitation']=[]
        if my_forms['case_study_form'].is_valid() and my_forms['host_form'].is_valid() and my_forms['pest_form'].is_valid() and my_forms['weather_form'].is_valid():
            required_models['new_case_study'] = my_forms['case_study_form'].save(commit=False)
            required_models['new_host'] = my_forms['host_form'].save(commit=False)
            required_models['new_pest'] = my_forms['pest_form'].save(commit=False)
            required_models['new_weather'] = my_forms['weather_form'].save(commit=False)
            success=True
            if required_models['new_host'].mortality_on == True:
                if my_forms['mortality_form'].is_valid():
                    required_models['new_mortality'] = my_forms['mortality_form'].save(commit=False)
                    optional_models['host'].append(required_models['new_mortality'])
                else:
                    success = False
            if required_models['new_pest'].vector_born == True:
                if my_forms['vector_form'].is_valid():
                    required_models['new_vector'] = my_forms['vector_form'].save(commit=False)
                    optional_models['pest'].append(required_models['new_vector'])
                else:
                    success = False
            if required_models['new_weather'].wind_on == True:
                if my_forms['wind_form'].is_valid():
                    required_models['new_wind'] = my_forms['wind_form'].save(commit=False)
                    optional_models['weather'].append(required_models['new_wind'])
                else:
                    success = False
            if required_models['new_weather'].seasonality_on == True:
                if my_forms['seasonality_form'].is_valid():
                    required_models['new_seasonality'] = my_forms['seasonality_form'].save(commit=False)
                    optional_models['weather'].append(required_models['new_seasonality'])
                else:
                    success = False
            if required_models['new_weather'].lethal_temp_on == True:
                if my_forms['lethal_temp_form'].is_valid():
                    required_models['new_lethal_temp'] = my_forms['lethal_temp_form'].save(commit=False)
                    optional_models['weather'].append(required_models['new_lethal_temp'])
                else:
                    success = False
            if required_models['new_weather'].temp_on == True:
                if my_forms['temperature_form'].is_valid():
                    required_models['new_temperature'] = my_forms['temperature_form'].save(commit=False)
                    optional_models['weather'].append(required_models['new_temperature'])
                    if required_models['new_temperature'].method == "POLYNOMIAL":
                        if my_forms['temperature_polynomial_form'].is_valid():
                            required_models['new_temperature_polynomial'] = my_forms['temperature_polynomial_form'].save(commit=False)
                            optional_models['temperature'].append(required_models['new_temperature_polynomial'])
                        else:
                            success = False
                    if required_models['new_temperature'].method == "RECLASS":
                        if my_forms['temperature_reclass_formset'].is_valid():
                            print("temp Reclass formset is valid")
                            reclass_forms = my_forms['temperature_reclass_formset'].save(commit=False)
                            for obj in my_forms['temperature_reclass_formset'].deleted_objects:
                                obj.delete()
                            for instance in reclass_forms:
                                optional_models['temperature'].append(instance)
                                print("instance stuff happened")
                                print(instance.min_value)
                        else:
                            success = False
                            print("Temp reclass formset form is INVALID")
                else:
                    success = False
            if required_models['new_weather'].precipitation_on == True:
                if my_forms['precipitation_form'].is_valid():
                    required_models['new_precipitation'] = my_forms['precipitation_form'].save(commit=False)
                    optional_models['weather'].append(required_models['new_precipitation'])
                    if required_models['new_precipitation'].method == "POLYNOMIAL":
                        if my_forms['precipitation_polynomial_form'].is_valid():
                            required_models['new_precipitation_polynomial'] = my_forms['precipitation_polynomial_form'].save(commit=False)
                            optional_models['precipitation'].append(required_models['new_precipitation_polynomial'])
                        else:
                            success = False
                    if required_models['new_precipitation'].method == "RECLASS":
                        if my_forms['precipitation_reclass_formset'].is_valid():
                            print("temp Reclass formset is valid")
                            reclass_forms = my_forms['precipitation_reclass_formset'].save(commit=False)
                            for obj in my_forms['precipitation_reclass_formset'].deleted_objects:
                                obj.delete()
                            for instance in reclass_forms:
                                optional_models['precipitation'].append(instance)
                                print("instance stuff happened")
                                print(instance.min_value)
                        else:
                            success = False
                            print("Temp reclass formset form is INVALID")                
                else:
                    success = False
        else:
            print('VALIDATION FAILED')
            success=False

        return required_models, success, optional_models

    def save_forms(self, request, required_models, success, optional_models):
        required_models['new_case_study'].created_by = request.user
        required_models['new_case_study'].save()
        required_models['new_host'].case_study = required_models['new_case_study']
        required_models['new_host'].save()
        required_models['new_pest'].case_study = required_models['new_case_study']
        required_models['new_pest'].save()
        required_models['new_weather'].case_study = required_models['new_case_study']
        required_models['new_weather'].save()
        for model in optional_models['host']:
            model.host = required_models['new_host']
            model.save()
        for model in optional_models['pest']:
            model.pest = required_models['new_pest']
            model.save()
        for model in optional_models['weather']:
            model.weather = required_models['new_weather']
            model.save()
        for model in optional_models['temperature']:
            model.temperature = required_models['new_temperature']
            model.save()
        for model in optional_models['precipitation']:
            model.precipitation = required_models['new_precipitation']
            model.save()

        return required_models

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
             permission = self.check_permissions(request, pk=pk)
             if not permission:
                 return HttpResponseForbidden()
        my_forms, database_content =self.initialize_forms(request, pk=pk)
        context ={**my_forms, **database_content}
        return self.render_to_response(context) 
        #return self.post(request, *args, **kwargs)

class ExtendCaseStudyView(NewCaseStudyView):

    def save_forms(self, request, required_models, success):
        original_case_study = get_object_or_404(CaseStudy, pk=self.kwargs.get('pk'))  
        required_models['new_case_study'].created_by = request.user
        required_models['new_case_study'].use_external_calibration = True      
        required_models['new_case_study'].calibration = original_case_study     
        required_models['new_case_study'].pk = None
        required_models['new_case_study'].save()
        required_models['new_host'].pk = None
        required_models['new_host'].case_study = required_models['new_case_study']
        required_models['new_host'].save()
        return required_models

    def check_permissions(self, request, pk):
        cs = get_object_or_404(CaseStudy, pk=pk)
        if cs.created_by == request.user or cs.staff_approved == True:
            return True
        return
        
class ApprovedCaseStudyListView(ListView):

    model = CaseStudy
    context_object_name = 'case_studies'
    #paginate_by = 10  # if pagination is desired
    template_name = 'pops/my_account.html'

    def get_queryset(self):
        return CaseStudy.objects.filter(staff_approved = True ).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CreateCaseStudyStart(ApprovedCaseStudyListView):

    template_name = 'pops/create_case_study_start.html'

    def post(self, request, **kwargs):
        case_study_id = request.POST.get('case_study_id')
        return redirect(reverse('case_study_edit', args=(case_study_id,)))

class ApprovedAndUserCaseStudyListView(ApprovedCaseStudyListView):
    
    #paginate_by = 5  # if pagination is desired
    template_name = 'pops/case_study_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_case_studies = CaseStudy.objects.filter(created_by = self.request.user).order_by('-pest__pest_information')
        context['user_case_studies'] = user_case_studies
        return context
    # def get_queryset(self):
    #     return CaseStudy.objects.filter(Q(staff_approved = True ) | Q(created_by = self.request.user))

#@login_required
def create_case_study(request):

    custom_error = []
    #Initialize all of the forms
    case_study_form = CaseStudyForm(prefix="cs")
    host_form = HostForm(prefix="host")

    #If the user has submitted the form
    if request.method == "POST":

        host_optional_models = []
        pest_optional_models = []
        weather_optional_models = []
        temperature_optional_models = []
        precipitation_optional_models = []

        case_study_form = CaseStudyForm(request.POST, request.FILES, prefix="cs")
        host_form = HostForm(request.POST, request.FILES, prefix="host")
        success=[]
        if case_study_form.is_valid() and host_form.is_valid():
            new_case_study = case_study_form.save(commit=False)
            new_host = host_form.save(commit=False)
            success=True
        else:
            success=False
        if success:
            print("Success!")
            print(success)
            new_case_study.created_by = request.user
            new_case_study.save()
            new_host.case_study = new_case_study
            new_host.save()
            #If successful, send the user to a page showing all of the case study details.
            return redirect('case_study_review', pk=new_case_study.pk)
        else:
            print("Something went wrong.")
            custom_error.append("Please correct the errors below:")
    else:
        print("Not a POST")
    #Context is a dictionary of data to pass to the template
    context = {
        'case_study_form': case_study_form,
        'host_form': host_form,
        'error_message': custom_error,
        }
    return render(request, 'pops/create_case_study2.html', context)

def case_study_edit(request,pk=None):
    host=[]
    case_study = []
    custom_error = []
    #Initialize all of the forms
    if pk:
        cs = get_object_or_404(CaseStudy, pk=pk)
        host = get_object_or_404(Host, case_study=cs)
        case_study_form = CaseStudyForm(prefix="cs", instance=cs)
        host_form = HostForm(prefix="host", instance=host)
        if cs.created_by != request.user:
            return HttpResponseForbidden()
    else:
        case_study_form = CaseStudyForm(prefix="cs")
        host_form = HostForm(prefix="host")

    #If the user has submitted the form
    if request.method == "POST":

        host_optional_models = []
        pest_optional_models = []
        weather_optional_models = []
        temperature_optional_models = []
        precipitation_optional_models = []
        if pk:
            cs = get_object_or_404(CaseStudy, pk=pk)
            host = get_object_or_404(Host, case_study=cs)
            case_study_form = CaseStudyForm(request.POST, request.FILES, prefix="cs",instance=cs)
            host_form = HostForm(request.POST, request.FILES, prefix="host", instance=host)
            if cs.created_by != request.user:
                return HttpResponseForbidden()
        else:
            case_study_form = CaseStudyForm(request.POST, request.FILES, prefix="cs")
            host_form = HostForm(request.POST, request.FILES, prefix="host")

        if case_study_form.is_valid() and host_form.is_valid():
            new_case_study = case_study_form.save(commit=False)
            new_host = host_form.save(commit=False)
            success=True
        else:
            success=False
        if success:
            print("Success!")
            print(success)
            new_case_study.created_by = request.user
            #new_case_study.pk = None
            new_case_study.save()
            #new_host.pk = None
            new_host.case_study = new_case_study
            new_host.save()
            #If successful, send the user to a page showing all of the case study details.
            return redirect('case_study_review', pk=new_case_study.pk)
        else:
            print("Something went wrong.")
            custom_error.append("Please correct the errors below:")
    else:
        print("Not a POST")
    #Context is a dictionary of data to pass to the template
    context = {
        'case_study_form': case_study_form,
        'host_form': host_form,
        'error_message': custom_error,
        }
    return render(request, 'pops/create_case_study2.html', context)



def case_study_submitted(request):
    return render(request, 'pops/case_study_submitted.html',)

import plotly.offline as opy
import plotly.graph_objs as go
import numpy as np

class SomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = "__all__"

class CaseStudyDetailView(DetailView):

    model = CaseStudy
    template_name = 'pops/case_study_details.html'

def case_study_details(request, pk):
    case_study = get_object_or_404(CaseStudy, pk=pk)
    class HostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Host
            fields = "__all__"
    class CaseStudySerializer(serializers.ModelSerializer):
        hosts=HostSerializer(many=True, read_only=True)
        class Meta:
            model = CaseStudy
            fields = "__all__"
            print(fields)

    casestudy = CaseStudySerializer(case_study).data
    return render(request, 'pops/case_study_details.html', {'case_study': case_study, 'casestudy': casestudy })#,'graph':graph})

def case_study_review(request, pk):
    case_study = CaseStudy.objects.select_related('weather').get(pk=pk) #get_object_or_404(CaseStudy, pk=pk)
    hosts = Host.objects.filter(case_study__pk=pk)
    pests = Pest.objects.filter(case_study__pk=pk).select_related('pest_information')
    context={}
    context['case_study'] = case_study
    context['hosts'] = hosts
    context['pests'] = pests
    temp_data=[]
    precip_data=[]
    if case_study.weather.temp_on:
        if case_study.weather.temperature.method == "RECLASS":
            for row in case_study.weather.temperature.temperaturereclass_set.all():
                temp_data.append(go.Scatter(x=[row.min_value, row.max_value], y=[row.reclass, row.reclass],
                    marker = dict(
                        size = 4,
                        color = 'black',
                        line = dict(
                            width = 1,
                            color = 'cyan'
                        )
                    ),
                    line = dict(
                            width = 2,
                            color = 'cyan'
                    )
                ))
                temp_data.append(go.Scatter(x=[row.min_value], y=[row.reclass],        
                    marker = dict(
                        size = 4,
                        color = 'cyan',
                        line = dict(
                            width = 1,
                            color = 'cyan'
                        )
                    ),
                ))
        if case_study.weather.temperature.method == "POLYNOMIAL":
            a0=case_study.weather.temperature.temperaturepolynomial.a0
            a1=case_study.weather.temperature.temperaturepolynomial.a1
            a2=case_study.weather.temperature.temperaturepolynomial.a2
            a3=case_study.weather.temperature.temperaturepolynomial.a3
            x1=case_study.weather.temperature.temperaturepolynomial.x1
            x2=case_study.weather.temperature.temperaturepolynomial.x2
            x3=case_study.weather.temperature.temperaturepolynomial.x3

            N = 100
            random_x = np.linspace(0, 100, 100)
            random_y0 = float(a0) + float(a1)*(random_x+float(x1))+float(a2)*(random_x+float(x2))**2

            # Create traces
            temp_data.append(go.Scatter(
                x = random_x,
                y = random_y0,
                mode = 'lines',
                line = dict(
                    width = 2,
                    color = 'cyan'
                )
            ))
        temp_graph=opy.plot({
            "data": temp_data,
            "layout": go.Layout(showlegend= False, 
                xaxis=dict(range=[-50, 50],showgrid=False, tickfont=dict(color='white'),title='Temperature (deg C)',titlefont=dict(color='white')), 
                yaxis=dict(range=[-0.1, 1.1], showgrid=False, tickfont=dict(color='white'),title='Reclass',titlefont=dict(color='white')), 
                width=300, height=200, 
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=go.layout.Margin(
                    l=50,
                    r=10,
                    b=40,
                    t=20,
                    pad=4
                    ),
                ),
            }, auto_open=False, output_type='div', config={"displayModeBar": False}
        )
        context['temp_graph'] = temp_graph
            
    if case_study.weather.precipitation_on:
        if case_study.weather.precipitation.method == "RECLASS":
            for row in case_study.weather.precipitation.precipitationreclass_set.all():
                precip_data.append(go.Scatter(x=[row.min_value, row.max_value], y=[row.reclass, row.reclass],
                    marker = dict(
                        size = 10,
                        color = 'black',
                        line = dict(
                            width = 2,
                            color = 'cyan'
                        )
                    ),
                    line = dict(
                            width = 2,
                            color = 'cyan'
                    )
                ))
                precip_data.append(go.Scatter(x=[row.min_value], y=[row.reclass],        
                    marker = dict(
                        size = 10,
                        color = 'cyan',
                        line = dict(
                            width = 2,
                            color = 'cyan'
                        )
                    ),
                ))
        if case_study.weather.precipitation.method == "POLYNOMIAL":
            a0=case_study.weather.precipitation.precipitationpolynomial.a0
            a1=case_study.weather.precipitation.precipitationpolynomial.a1
            a2=case_study.weather.precipitation.precipitationpolynomial.a2
            a3=case_study.weather.precipitation.precipitationpolynomial.a3
            x1=case_study.weather.precipitation.precipitationpolynomial.x1
            x2=case_study.weather.precipitation.precipitationpolynomial.x2
            x3=case_study.weather.precipitation.precipitationpolynomial.x3

            N = 100
            random_x = np.linspace(0, 100, 100)
            random_y0 = float(a0) + float(a1)*(random_x+float(x1))+float(a2)*(random_x+float(x2))**2

            # Create traces
            precip_data.append(go.Scatter(
                x = random_x,
                y = random_y0,
                mode = 'lines',
                line = dict(
                    width = 2,
                    color = 'cyan'
                )
            ))
        precip_graph=opy.plot({
            "data": precip_data,
            "layout": go.Layout(showlegend= False, 
                xaxis=dict(range=[0, 100],showgrid=False, tickfont=dict(color='white'),title='Precipitation (mm)',titlefont=dict(color='white')), 
                yaxis=dict(range=[0, 1], showgrid=False, tickfont=dict(color='white'),title='Reclass',titlefont=dict(color='white')), 
                width=300, height=200, 
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=go.layout.Margin(
                    l=50,
                    r=10,
                    b=40,
                    t=20,
                    pad=4
                    ),
                ),
            }, auto_open=False, output_type='div', config={"displayModeBar": False}
        )
        context['precip_graph'] = precip_graph
    return render(request, 'pops/case_study_review.html', context)

def plotly_test(request):
    return render(request, 'pops/plotly_test.html',)

import plotly.offline as opy
import plotly.graph_objs as go

class Graph(TemplateView):
    template_name = 'pops/plotly_test.html'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)


        div=opy.plot({
            "data": [go.Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
            "layout": go.Layout(title="hello world")
        }, auto_open=False, output_type='div')


        context['graph'] = div

        return context


