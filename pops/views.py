from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms import ModelForm
from .models import *
from .forms import *

#@login_required
def create_case_study(request):
    custom_error = []

    case_study_form = CaseStudyForm(prefix="cs")
    host_form = HostForm(prefix="host")
    mortality_form = MortalityForm(prefix="mortality")
    pest_form = PestForm(prefix="pest")
    vector_form = VectorForm(prefix="vector")
    weather_form = WeatherForm(prefix="weather")
    wind_form = WindForm(prefix="wind")
    seasonality_form = SeasonalityForm(prefix="seasonality")
    lethal_temp_form = LethalTemperatureForm(prefix="lethal_temp")
    temperature_form = TemperatureForm(prefix="temp")
    precipitation_form = PrecipitationForm(prefix="precip")
    temperature_reclass_form = TemperatureReclassForm(prefix="temp_reclass")
    precipitation_reclass_form = PrecipitationReclassForm(prefix="precip_reclass")
    temperature_polynomial_form = TemperaturePolynomialForm(prefix="temp_polynomial")
    precipitation_polynomial_form = PrecipitationPolynomialForm(prefix="precip_polynomial")

    if request.method == "POST":
        
        host_success_models = []
        pest_success_models = []
        weather_success_models = []
        temperature_success_models = []
        precipitation_success_models = []

        case_study_form = CaseStudyForm(request.POST, prefix="cs")
        host_form = HostForm(request.POST, prefix="host")
        pest_form = PestForm(request.POST, prefix="pest")
        weather_form = WeatherForm(request.POST, prefix="weather")

        if case_study_form.is_valid() and host_form.is_valid() and pest_form.is_valid() and weather_form.is_valid():
            new_case_study = case_study_form.save(commit=False)
            new_host = host_form.save(commit=False)
            new_pest = pest_form.save(commit=False)
            new_weather = weather_form.save(commit=False)
            success = True
            if new_host.mortality_on == True:
                mortality_form = MortalityForm(request.POST, prefix="mortality")
                if mortality_form.is_valid():
                    print("Mortality form is valid")
                    new_mortality = mortality_form.save(commit=False)
                    host_success_models.append(new_mortality)
                else:
                    success = False
                    print("Mortality form is INVALID")

            if new_pest.vector_born == True:
                vector_form = VectorForm(request.POST, prefix="vector")
                if vector_form.is_valid():
                    print("Vector form is valid")
                    new_vector = vector_form.save(commit=False)
                    pest_success_models.append(new_vector)
                else:
                    success = False
                    print("Vector form is INVALID")

            if new_weather.wind_on == True:
                wind_form = WindForm(request.POST, prefix="wind")
                if wind_form.is_valid():
                    print("Wind form is valid")
                    new_wind = wind_form.save(commit=False)
                    weather_success_models.append(new_wind)
                else:
                    success = False
                    print("Wind form is INVALID")

            if new_weather.seasonality_on == True:
                seasonality_form = SeasonalityForm(request.POST, prefix="seasonality")
                if seasonality_form.is_valid():
                    print("Seasonality form is valid")
                    new_seasonality = seasonality_form.save(commit=False)
                    weather_success_models.append(new_seasonality)
                else:
                    success = False
                    print("Seasonality form is INVALID")

            if new_weather.lethal_temp_on == True:
                lethal_temp_form = LethalTemperatureForm(request.POST, prefix="lethal_temp")
                if lethal_temp_form.is_valid():
                    print("Lethal temp form is valid")
                    new_lethal_temp = lethal_temp_form.save(commit=False)
                    weather_success_models.append(new_lethal_temp)
                else:
                    success = False
                    print("Lethal Temp form is INVALID")

            if new_weather.temp_on == True:
                temperature_form = TemperatureForm(request.POST, prefix="temp")
                if temperature_form.is_valid():
                    print("Temp form is valid")
                    new_temperature = temperature_form.save(commit=False)
                    weather_success_models.append(new_temperature)
                    if new_temperature.method == "RECLASS":
                        temperature_reclass_form = TemperatureReclassForm(request.POST, prefix="temp_reclass")
                        if temperature_reclass_form.is_valid():
                            print("Temp Reclass form is valid")
                            new_temperature_reclass = temperature_reclass_form.save(commit=False)
                            temperature_success_models.append(new_temperature_reclass)
                        else:
                            success = False
                            print("Temp reclass form is INVALID")
                    if new_temperature.method == "POLYNOMIAL":
                        temperature_polynomial_form = TemperaturePolynomialForm(request.POST, prefix="temp_polynomial")
                        if temperature_polynomial_form.is_valid():
                            print("Temp Polynomial form is valid")
                            new_temperature_polynomial = temperature_polynomial_form.save(commit=False)
                            temperature_success_models.append(new_temperature_polynomial)
                        else:
                            success = False
                            print("Temp Polynomial form is INVALID")
                else:
                    success = False
                    print("Temp form is INVALID")

            if new_weather.precipitation_on == True:
                precipitation_form = PrecipitationForm(request.POST, prefix="precip")
                if precipitation_form.is_valid():
                    print("Precipitation form is valid")
                    new_precipitation = precipitation_form.save(commit=False)
                    weather_success_models.append(new_precipitation)
                    if new_precipitation.method == "RECLASS":
                        precipitation_reclass_form = PrecipitationReclassForm(request.POST, prefix="precip_reclass")
                        if precipitation_reclass_form.is_valid():
                            print("Precip Reclass form is valid")
                            new_precipitation_reclass = precipitation_reclass_form.save(commit=False)
                            precipitation_success_models.append(new_precipitation_reclass)
                        else:
                            success = False
                            print("Precip reclass form is INVALID")
                    if new_precipitation.method == "POLYNOMIAL":
                        precipitation_polynomial_form = PrecipitationPolynomialForm(request.POST, prefix="precip_polynomial")
                        if precipitation_polynomial_form.is_valid():
                            print("precipitation Polynomial form is valid")
                            new_precipitation_polynomial = precipitation_polynomial_form.save(commit=False)
                            precipitation_success_models.append(new_precipitation_polynomial)
                        else:
                            success = False
                            print("Temp Polynomial form is INVALID")
                else:
                    success = False
                    print("Precipitation form is INVALID")
        else:
            success = False
        if success:
            print("Success!")
            print(success)
            new_case_study.save()
            new_host.save()
            new_host.case_study.add(new_case_study)
            new_pest.save()
            new_pest.case_study.add(new_case_study)
            new_weather.case_study = new_case_study
            new_weather.save()
            for model in host_success_models:
                model.host = new_host
                model.save()
            for model in pest_success_models:
                model.pest = new_pest
                model.save()
            for model in weather_success_models:
                model.weather = new_weather
                model.save()
            for model in temperature_success_models:
                model.temperature = new_temperature
                model.save()
            for model in precipitation_success_models:
                model.precipitation = new_precipitation
                model.save()
            return redirect('case_study_details', pk=new_case_study.pk)
        else:
            print("Something went wrong.")
            custom_error.append("Please correct the errors below:")
    else:
        print("Not a POST")
    return render(request, 'pops/create_case_study.html',{'case_study_form': case_study_form, 'host_form': host_form, 'mortality_form': mortality_form, 'pest_form': pest_form, 'vector_form': vector_form, 'weather_form': weather_form, 'wind_form': wind_form, 'seasonality_form': seasonality_form, 'lethal_temp_form': lethal_temp_form, 'temperature_form': temperature_form, 'precipitation_form': precipitation_form, 'temperature_reclass_form': temperature_reclass_form, 'precipitation_reclass_form': precipitation_reclass_form, 'temperature_polynomial_form': temperature_polynomial_form, 'precipitation_polynomial_form': precipitation_polynomial_form, 'error_message': custom_error})# 'short_distance_form': short_distance_form, 'long_distance_form': long_distance_form, 'cryptic_to_infected_form': cryptic_to_infected_form, 'infected_to_diseased_form': infected_to_diseased_form, 'weather_form': weather_form, 'wind_form': wind_form, 'seasonality_form': seasonality_form, 'lethal_temp_form': lethal_temp_form, 'temperature_form': temperature_form, 'precipitation_form': precipitation_form, 'temperature_reclass_form': temperature_reclass_form, 'precipitation_reclass_form': precipitation_reclass_form, 'temperature_polynomial_form': temperature_polynomial_form, 'precipitation_polynomial_form': precipitation_polynomial_form})


def case_study_submitted(request):
    return render(request, 'pops/case_study_submitted.html',)

def case_study_details(request, pk):
    case_study = get_object_or_404(CaseStudy, pk=pk)

    class CaseStudyAllForm(ModelForm):
        class Meta:
            model = CaseStudy
            fields = '__all__'

    data = CaseStudyAllForm(instance=case_study)
    return render(request, 'pops/case_study_details.html', {'case_study': case_study, 'data': data})

