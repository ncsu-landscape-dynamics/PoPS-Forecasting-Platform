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

@login_required
def create_case_study(request):
    case_study_form = CaseStudyForm(prefix="cs")
    host_form = HostForm(prefix="host")
    pest_form = PestForm(prefix="pest")
    mortality_form = MortalityForm(prefix="mortality")
    vector_form = VectorForm(prefix="vector")
    short_distance_form = ShortDistanceForm(prefix="short")
    long_distance_form = LongDistanceForm(prefix="long")
    cryptic_to_infected_form = CrypticToInfectedForm(prefix="cryptic_to_infected")
    infected_to_diseased_form = InfectedToDiseasedForm(prefix="infected_to_diseased")
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
        case_study_form = CaseStudyForm(request.POST, prefix="cs")
        host_form = HostForm(request.POST, prefix="host")
        mortality_form = MortalityForm(request.POST, prefix="mortality")
        pest_form = PestForm(request.POST, prefix="pest")
        vector_form = VectorForm(request.POST, prefix="vector")
        short_distance_form = ShortDistanceForm(request.POST, prefix="short")
        long_distance_form = LongDistanceForm(request.POST, prefix="long")
        cryptic_to_infected_form = CrypticToInfectedForm(request.POST, prefix="cryptic_to_infected")
        infected_to_diseased_form = InfectedToDiseasedForm(request.POST, prefix="infected_to_diseased")
        weather_form = WeatherForm(request.POST, prefix="weather")
        wind_form = WindForm(request.POST, prefix="wind")
        seasonality_form = SeasonalityForm(request.POST, prefix="seasonality")
        lethal_temp_form = LethalTemperatureForm(request.POST, prefix="lethal_temp")
        temperature_form = TemperatureForm(request.POST, prefix="temp")
        precipitation_form = PrecipitationForm(request.POST, prefix="precip")
        temperature_reclass_form = TemperatureReclassForm(request.POST, prefix="temp_reclass")
        precipitation_reclass_form = PrecipitationReclassForm(request.POST, prefix="precip_reclass")
        temperature_polynomial_form = TemperaturePolynomialForm(request.POST, prefix="temp_polynomial")
        precipitation_polynomial_form = PrecipitationPolynomialForm(request.POST, prefix="precip_polynomial")

        if case_study_form.is_valid() and host_form.is_valid() and mortality_form.is_valid() and pest_form.is_valid() and short_distance_form.is_valid() and long_distance_form.is_valid() and cryptic_to_infected_form.is_valid() and infected_to_diseased_form.is_valid() and wind_form.is_valid() and seasonality_form.is_valid() and lethal_temp_form.is_valid() and temperature_form.is_valid() and precipitation_form.is_valid() and temperature_reclass_form.is_valid() and precipitation_reclass_form.is_valid() and temperature_polynomial_form.is_valid() and precipitation_polynomial_form.is_valid():
            new_case_study = case_study_form.save(commit=False)
            new_case_study.save()
            new_host = host_form.save()
            new_host.case_study.add(new_case_study)
            new_host.save()
            new_mortality = mortality_form.save(commit=False)
            new_mortality.host = new_host
            new_mortality.save()
            new_pest = pest_form.save()
            new_pest.case_study.add(new_case_study)
            new_pest.save()
            new_vector = vector_form.save(commit=False)
            new_vector.pest = new_pest
            new_vector.save()
            new_short_distance = short_distance_form.save(commit=False)
            new_short_distance.pest = new_pest
            new_short_distance.save()
            new_long_distance = long_distance_form.save(commit=False)
            new_long_distance.pest = new_pest
            new_long_distance.save()
            new_cryptic_to_infected = cryptic_to_infected_form.save(commit=False)
            new_cryptic_to_infected.pest = new_pest
            new_cryptic_to_infected.save()
            new_infected_to_diseased = infected_to_diseased_form.save(commit=False)
            new_infected_to_diseased.pest = new_pest
            new_infected_to_diseased.save()
            new_weather = weather_form.save(commit=False)
            new_weather.case_study = new_case_study
            new_weather.save()
            new_wind = wind_form.save(commit=False)
            new_wind.weather = new_weather
            new_wind.save()
            new_seasonality = seasonality_form.save(commit=False)
            new_seasonality.weather = new_weather
            new_seasonality.save()
            new_lethal_temp = lethal_temp_form.save(commit=False)
            new_lethal_temp.weather = new_weather
            new_lethal_temp.save()
            new_temperature = temperature_form.save(commit=False)
            new_temperature.weather = new_weather
            new_temperature.save()
            new_precipitation = precipitation_form.save(commit=False)
            new_precipitation.weather = new_weather
            new_precipitation.save()
            new_temp_reclass = temperature_reclass_form.save(commit=False)
            new_temp_reclass.temperature = new_temperature
            new_temp_reclass.save()
            new_precip_reclass = precipitation_reclass_form.save(commit=False)
            new_precip_reclass.precipitation = new_precipitation
            new_precip_reclass.save()
            new_temp_polynomial = temperature_polynomial_form.save(commit=False)
            new_temp_polynomial.temperature = new_temperature
            new_temp_polynomial.save()
            new_precip_polynomial = precipitation_polynomial_form.save(commit=False)
            new_precip_polynomial.precipitation = new_precipitation
            new_precip_polynomial.save()
            return redirect('case_study_submitted')
    else:
        case_study_form = CaseStudyForm(prefix="cs")
        host_form = HostForm(prefix="host")
        mortality_form = MortalityForm(prefix="mortality")
        pest_form = PestForm(prefix="pest")
        vector_form = VectorForm(prefix="vector")
        short_distance_form = ShortDistanceForm(prefix="short")
        long_distance_form = LongDistanceForm(prefix="long")
        cryptic_to_infected_form = CrypticToInfectedForm(prefix="cryptic_to_infected")
        infected_to_diseased_form = InfectedToDiseasedForm(prefix="infected_to_diseased")
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

    return render(request, 'pops/create_case_study.html',{'case_study_form': case_study_form, 'host_form': host_form, 'mortality_form': mortality_form, 'pest_form': pest_form, 'vector_form': vector_form, 'short_distance_form': short_distance_form, 'long_distance_form': long_distance_form, 'cryptic_to_infected_form': cryptic_to_infected_form, 'infected_to_diseased_form': infected_to_diseased_form, 'weather_form': weather_form, 'wind_form': wind_form, 'seasonality_form': seasonality_form, 'lethal_temp_form': lethal_temp_form, 'temperature_form': temperature_form, 'precipitation_form': precipitation_form, 'temperature_reclass_form': temperature_reclass_form, 'precipitation_reclass_form': precipitation_reclass_form, 'temperature_polynomial_form': temperature_polynomial_form, 'precipitation_polynomial_form': precipitation_polynomial_form})


def case_study_submitted(request):
    return render(request, 'pops/case_study_submitted.html',)

def case_study_details(request, pk):
    case_study = get_object_or_404(CaseStudy, pk=pk)

    class CaseStudyAllForm(ModelForm):
        class Meta:
            model = CaseStudy
            fields = '__all__'

    data = CaseStudyAllForm(instance=case_study)
    #data = serializers.serialize( "python", CaseStudy.objects.all())
    return render(request, 'pops/case_study_details.html', {'case_study': case_study, 'data': data})


