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
        my_forms=self.initialize_forms(request, pk=pk)
        instances, success = self.validate_forms(my_forms)
        if success:
            instances = self.save_forms(request, instances, success)
            return redirect('case_study_review2', pk=instances['new_case_study'].pk)
        else:
            my_forms['error_message'] = "Please correct the errors below:"    
        return self.render_to_response(my_forms) 

    def check_permissions(self, request, pk):
        cs = get_object_or_404(CaseStudy, pk=pk)
        if cs.created_by == request.user:
            return True
        return

    def initialize_forms(self, request, pk=None):
        my_forms={}
        post_data = request.POST or None
        file_data = request.FILES or None
        cs=None
        host=None
        mortality=None
        if pk:
            cs = get_object_or_404(CaseStudy, pk=pk)
            host = get_object_or_404(Host, case_study=cs)
        my_forms['case_study_form'] = CaseStudyForm(post_data, file_data, instance=cs, prefix='cs')
        my_forms['host_form'] = HostForm(post_data, file_data, instance=host, prefix='host')
        return my_forms

    def validate_forms(self, my_forms):
        instances={}
        if my_forms['case_study_form'].is_valid() and my_forms['host_form'].is_valid():
            instances['new_case_study'] = my_forms['case_study_form'].save(commit=False)
            instances['new_host'] = my_forms['host_form'].save(commit=False)
            success=True
        else:
            success=False
        return instances, success

    def save_forms(self, request, instances, success):
        instances['new_case_study'].created_by = request.user
        instances['new_case_study'].save()
        instances['new_host'].case_study = instances['new_case_study']
        instances['new_host'].save()
        #If successful, send the user to a page showing all of the case study details.
        return instances

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
             permission = self.check_permissions(request, pk=pk)
             if not permission:
                 return HttpResponseForbidden()
        my_forms=self.initialize_forms(request, pk=pk)
        return self.render_to_response(my_forms) 
        #return self.post(request, *args, **kwargs)

class ExtendCaseStudyView(NewCaseStudyView):

    def save_forms(self, request, instances, success):
        original_case_study = get_object_or_404(CaseStudy, pk=self.kwargs.get('pk'))  
        instances['new_case_study'].created_by = request.user
        instances['new_case_study'].use_external_calibration = True      
        instances['new_case_study'].calibration = original_case_study     
        instances['new_case_study'].pk = None
        instances['new_case_study'].save()
        instances['new_host'].pk = None
        instances['new_host'].case_study = instances['new_case_study']
        instances['new_host'].save()
        return instances

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

        host_success_models = []
        pest_success_models = []
        weather_success_models = []
        temperature_success_models = []
        precipitation_success_models = []

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

        host_success_models = []
        pest_success_models = []
        weather_success_models = []
        temperature_success_models = []
        precipitation_success_models = []
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


