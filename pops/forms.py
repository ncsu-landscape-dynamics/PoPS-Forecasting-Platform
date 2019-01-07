# pops/forms.py
from django import forms
#from .models import CaseStudy, Host, Mortality, Pest, Vector
from .models import *

class CaseStudyForm(forms.ModelForm):

    start_year = forms.DateField(widget=forms.DateInput(format='%Y'),input_formats=('%Y',))
    end_year = forms.DateField(widget=forms.DateInput(format='%Y'),input_formats=('%Y',))

    class Meta:
        model = CaseStudy
        fields = ['name','number_of_pests','number_of_hosts','start_year','end_year','time_step']

class HostForm(forms.ModelForm):

    class Meta:
        model = Host
        exclude = ['case_study']

class MortalityForm(forms.ModelForm):

    class Meta:
        model = Mortality
        exclude = ['host']

class PestForm(forms.ModelForm):

    class Meta:
        model = Pest
        exclude = ['case_study','pest_information','staff_approved']

class VectorForm(forms.ModelForm):

    class Meta:
        model = Vector
        exclude = ['pest']

class ShortDistanceForm(forms.ModelForm):

    class Meta:
        model = ShortDistance
        exclude = ['pest']

class LongDistanceForm(forms.ModelForm):

    class Meta:
        model = LongDistance
        exclude = ['pest']

class CrypticToInfectedForm(forms.ModelForm):

    class Meta:
        model = CrypticToInfected
        exclude = ['pest']

class InfectedToDiseasedForm(forms.ModelForm):

    class Meta:
        model = InfectedToDiseased
        exclude = ['pest']

class WeatherForm(forms.ModelForm):

    class Meta:
        model = Weather
        exclude = ['case_study']

class WindForm(forms.ModelForm):

    class Meta:
        model = Wind
        exclude = ['weather']

class SeasonalityForm(forms.ModelForm):

    class Meta:
        model = Seasonality
        exclude = ['weather']

class LethalTemperatureForm(forms.ModelForm):

    class Meta:
        model = LethalTemperature
        exclude = ['weather']

class TemperatureForm(forms.ModelForm):

    class Meta:
        model = Temperature
        exclude = ['weather']

class PrecipitationForm(forms.ModelForm):

    class Meta:
        model = Precipitation
        exclude = ['weather']

class TemperatureReclassForm(forms.ModelForm):

    class Meta:
        model = TemperatureReclass
        exclude = ['temperature']

class PrecipitationReclassForm(forms.ModelForm):

    class Meta:
        model = PrecipitationReclass
        exclude = ['precipitation']

class TemperaturePolynomialForm(forms.ModelForm):

    class Meta:
        model = TemperaturePolynomial
        exclude = ['temperature']

class PrecipitationPolynomialForm(forms.ModelForm):

    class Meta:
        model = PrecipitationPolynomial
        exclude = ['precipitation']
