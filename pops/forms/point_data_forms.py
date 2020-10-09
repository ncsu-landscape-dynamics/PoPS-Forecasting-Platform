# pops/forms.py
from django import forms
from django.forms import BaseInlineFormSet



from ..models import *

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

#function to convert "bytes" to human readable file size
def human_readable_size(num, suffix='B'):
    for unit in ['','K','M','G']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

#Validate the files are smaller than the max file size set in settings.py
def validate_file_size(self, fields):
    for field in fields:
        data_file = self.cleaned_data.get(field)
        if data_file:
            print('Data file is here')
            print(field)
            print(data_file)
            print(type(data_file))
            print(hasattr(data_file, 'instance'))
            if not hasattr(data_file, 'instance'):
                print('Instance check is true')
                if data_file.content_type in settings.CASE_STUDY_UPLOAD_FILE_TYPES:
                    if data_file.size > settings.CASE_STUDY_UPLOAD_FILE_MAX_SIZE:
                        msg = forms.ValidationError("File size must be less than %s. Selected file was: %s" % (human_readable_size(settings.CASE_STUDY_UPLOAD_FILE_MAX_SIZE), human_readable_size(data_file.size)))
                        self.add_error(field, msg)
                else:
                    msg = forms.ValidationError("File type must be TIFF (.tif)")
                    self.add_error(field, msg)

class PointDataForm(forms.ModelForm):
    fields_required = fields_required_conditionally
    validate_size = validate_file_size

    class Meta:
        model = Point
        fields = ['count','point']

    def clean(self):
        self.fields_required(['count'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(PointDataForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})


