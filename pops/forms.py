# pops/forms.py
from django import forms

from .models import *

from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab, PrependedText, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, Row, HTML

def fields_required_conditionally(self, fields):
    """Used for conditionally marking fields as required."""
    for field in fields:
        value = self.cleaned_data.get(field, '')
        if not value and value != 0:
            msg = forms.ValidationError("This field is required.")
            self.add_error(field, msg)

class CaseStudyForm(forms.ModelForm):
    fields_required = fields_required_conditionally
    class Meta:
        model = CaseStudy
        fields = ['name','number_of_pests','number_of_hosts','start_year','end_year','future_years',
                'time_step','all_plants','infestation_data','use_treatment','treatment_data']

    def __init__(self, *args, **kwargs):
        super(CaseStudyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                Row(
                    Div(
                        Field('name', wrapper_class=""),
                            css_class='col-sm-12'
                        ),
                ),
                Row(
                    Div(
                        Field('start_year', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                    Div(
                        Field('end_year', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                ),
                Row(
                    Div(
                        Field('future_years', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                    Div(
                        Field('time_step', wrapper_class=""),
                            css_class='col-sm-6'
                        )
                ),
                Row(
                    Div(
                        Field('number_of_pests', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                    Div(
                        Field('number_of_hosts', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                ),
        )

    def clean(self):
        self.fields_required(['name','number_of_pests','number_of_hosts','start_year','end_year','time_step','future_years','all_plants','infestation_data'])
        use_treatment = self.cleaned_data.get('use_treatment')

        if use_treatment:
            self.fields_required(['treatment_data'])
        else:
            self.cleaned_data['treatment_data'] = ''

        return self.cleaned_data


class HostForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Host
        fields = ['name','score','host_data','mortality_on']

    def clean(self):
        self.fields_required(['name','score','host_data'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(HostForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                Row(
                    Div(
                        Field('name', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                    Div(
                        Field('score', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                ),

        )

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

    def __init__(self, *args, **kwargs):
        super(MortalityForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                Row(
                    Div(
                        Field('rate', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                    Div(
                        Field('time_lag', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                ),

        )

class PestForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Pest
        fields = ['pest_information','name','model_type','dispersal_type','vector_born']

    def clean(self):
        self.fields_required(['pest_information','model_type','dispersal_type'])
        pest_information = self.cleaned_data.get('pest_information')
        if pest_information:
            if pest_information.common_name == "Other":
                self.fields_required(['name'])
            else:
                self.cleaned_data['name'] = ''

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(PestForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                Row(
                    Div(
                        Field('pest_information', wrapper_class=""),
                            css_class='col-sm-12'
                        ),
                ),
                Row(
                    Div(
                        Field('name', wrapper_class=""),
                            css_class='col-sm-12'
                        ),
                ),
                Row(
                    Div(
                        Field('model_type', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                    Div(
                        Field('dispersal_type', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                ),
        )


class VectorForm(forms.ModelForm):
    fields_required = fields_required_conditionally
    
    class Meta:
        model = Vector
        fields = ['common_name','scientific_name']
    
    def clean(self):
        self.fields_required(['common_name','scientific_name'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(VectorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                Row(
                    Div(
                        Field('common_name', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                    Div(
                        Field('scientific_name', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                ),

            
        )

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

    def __init__(self, *args, **kwargs):
        super(WeatherForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

class WindForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Wind
        fields = ['wind_direction','kappa']

    def clean(self):
        self.fields_required(['wind_direction','kappa'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(WindForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                Row(
                    Div(
                        Field('wind_direction', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                    Div(
                        Field('kappa', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                ),

        )

class SeasonalityForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Seasonality
        fields = ['first_month','last_month']

    def clean(self):
        self.fields_required(['first_month','last_month'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(SeasonalityForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                Row(
                    Div(
                        Field('first_month', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                    Div(
                        Field('last_month', wrapper_class=""),
                            css_class='col-sm-6'
                        ),
                ),

        )

class LethalTemperatureForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = LethalTemperature
        fields = ['month','value']

    def clean(self):
        self.fields_required(['month','value'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(LethalTemperatureForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                Row(
                    Div(
                        Field('month'),
                            css_class='col-sm-8'
                        ),
                    Div(
                        Field(AppendedText('value', '&#176;C')),
                        HTML("{% for error in lethal_temp_form.value.errors %}<div class='py-0' style='color:red; font-size:0.8em'><strong>{{ error }}</strong></div>{% endfor %}"),
                            css_class='col-sm-4'
                        ),
                ),

        )

class TemperatureForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Temperature
        fields = ['method']
        
    def clean(self):
        self.fields_required(['method'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(TemperatureForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                            InlineRadios('method')        
                            )

class PrecipitationForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = Precipitation
        fields = ['method']

    def clean(self):
        self.fields_required(['method'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(PrecipitationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                            InlineRadios('method')        
                            )

class TemperatureReclassForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = TemperatureReclass
        fields = ['min_value','max_value','reclass']
    
    def clean(self):
        self.fields_required(['min_value','max_value','reclass'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(TemperatureReclassForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                Row(
                    Div(
                        Field('min_value', style=""),
                            css_class='col-3'
                        ),
                    Div(
                        Field('max_value', style=""),
                            css_class='col-3'
                        ),
                    Div(
                        Field('reclass', style=""),
                            css_class='col-3'
                        ),
                    #HTML('<div class="col-1 pb-3 px-1 input-group-append"><button class="btn btn-info add-form-row" style="font-size: 1em; max-height:2.5em;">+</button></div>'),
                )
        )

TemperatureReclassFormSet = forms.modelformset_factory(TemperatureReclass, form=TemperatureReclassForm, extra=1)

class PrecipitationReclassForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = PrecipitationReclass
        fields = ['min_value','max_value','reclass']
    
    def clean(self):
        self.fields_required(['min_value','max_value','reclass'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(PrecipitationReclassForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
                Row(
                    Div(
                        Field('min_value', style=""),
                            css_class='col-3'
                        ),
                    Div(
                        Field('max_value', style=""),
                            css_class='col-3'
                        ),
                    Div(
                        Field('reclass', style=""),
                            css_class='col-3'
                        ),
                    #HTML('<div class="col-1 pb-3 px-1 input-group-append"><button class="btn btn-info add-form-row" style="font-size: 1em; max-height:2.5em;">+</button></div>'),
                )
        )

PrecipitationReclassFormSet = forms.modelformset_factory(PrecipitationReclass, form=PrecipitationReclassForm, extra=1)

class TemperaturePolynomialForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = TemperaturePolynomial
        fields = ['degree','a0','a1','a2','a3','x1','x2','x3']

    def __init__(self, *args, **kwargs):
        super(TemperaturePolynomialForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        #self.helper.label_class = 'col-4 control-label'
        #self.helper.field_class = 'col-8'
        self.helper.layout = Layout(
                            InlineRadios('degree')        
                            )

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
   
    def __init__(self, *args, **kwargs):
        super(PrecipitationPolynomialForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        #self.helper.label_class = 'col-4 control-label'
        #self.helper.field_class = 'col-8'
        self.helper.layout = Layout(
                            InlineRadios('degree'),        
                            )

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

