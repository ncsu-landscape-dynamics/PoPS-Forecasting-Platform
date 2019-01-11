# pops/forms.py
from django import forms
from .models import *

def fields_required_conditionally(self, fields):
    """Used for conditionally marking fields as required."""
    for field in fields:
        if not self.cleaned_data.get(field, ''):
            msg = forms.ValidationError("This field is required.")
            self.add_error(field, msg)

class CaseStudyForm(forms.ModelForm):
    fields_required = fields_required_conditionally
    class Meta:
        model = CaseStudy
        fields = ['name','number_of_pests','number_of_hosts','start_year','end_year','time_step']

    def clean(self):
        self.fields_required(['name','number_of_pests','number_of_hosts','start_year','end_year','time_step'])
        return self.cleaned_data

class HostForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Host
        fields = ['name','score','mortality_on']

    def clean(self):
        self.fields_required(['name','score'])
        return self.cleaned_data

class MortalityForm(forms.ModelForm):
    fields_required = fields_required_conditionally
    class Meta:
        model = Mortality
        fields = ['user_input','rate','time_lag']
    
    def clean(self):
        user_input = self.cleaned_data.get('user_input')

        if user_input:
            self.fields_required(['rate','time_lag'])
        else:
            self.cleaned_data['rate','time_lag'] = ''

        return self.cleaned_data


class PestForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Pest
        fields = ['name','model_type','dispersal_type','vector_born']

    def clean(self):
        self.fields_required(['name','model_type','dispersal_type'])
        return self.cleaned_data

class VectorForm(forms.ModelForm):
    fields_required = fields_required_conditionally
    
    class Meta:
        model = Vector
        fields = ['common_name','scientific_name']
    
    def clean(self):
        self.fields_required(['common_name','scientific_name'])
        return self.cleaned_data


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
    fields_required = fields_required_conditionally

    class Meta:
        model = Weather
        fields = ['wind_on', 'seasonality_on','lethal_temp_on','temp_on','precipitation_on']


class WindForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Wind
        fields = ['wind_direction','kappa']

    def clean(self):
        self.fields_required(['wind_direction','kappa'])
        return self.cleaned_data

class SeasonalityForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Seasonality
        fields = ['first_month','last_month']

    def clean(self):
        self.fields_required(['first_month','last_month'])
        return self.cleaned_data

class LethalTemperatureForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = LethalTemperature
        fields = ['month','value']

    def clean(self):
        self.fields_required(['month','value'])
        return self.cleaned_data

class TemperatureForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Temperature
        fields = ['method']
        
    def clean(self):
        self.fields_required(['method'])
        return self.cleaned_data

class PrecipitationForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Precipitation
        fields = ['method']

    def clean(self):
        self.fields_required(['method'])
        return self.cleaned_data

class TemperatureReclassForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = TemperatureReclass
        fields = ['threshold']
    
    def clean(self):
        self.fields_required(['threshold'])
        return self.cleaned_data


class PrecipitationReclassForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = PrecipitationReclass
        fields = ['threshold']
    
    def clean(self):
        self.fields_required(['threshold'])
        return self.cleaned_data

class TemperaturePolynomialForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = TemperaturePolynomial
        fields = ['degree','a0','a1','a2','a3','x1','x2','x3']
    
    def clean(self):
        degree = self.cleaned_data.get('degree')
        self.fields_required(['degree'])
        if degree == 1:
            self.fields_required(['a0','a1','x1'])
        if degree == 2:
            self.fields_required(['a0','a1','a2','x1','x2'])
        if degree == 3:
            self.fields_required(['a0','a1','a2','a3','x1','x2','x3'])
        return self.cleaned_data

class PrecipitationPolynomialForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = PrecipitationPolynomial
        fields = ['degree','a0','a1','a2','a3','x1','x2','x3']

    def clean(self):
        degree = self.cleaned_data.get('degree')
        self.fields_required(['degree'])
        if degree == 1:
            self.fields_required(['a0','a1','x1'])
        if degree == 2:
            self.fields_required(['a0','a1','a2','x1','x2'])
        if degree == 3:
            self.fields_required(['a0','a1','a2','a3','x1','x2','x3'])
        return self.cleaned_data

