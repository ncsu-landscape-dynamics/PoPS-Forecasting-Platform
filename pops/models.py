from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
import os
# from matrix_field import MatrixField

from users.models import CustomUser


# Django automatically creates a primary key for each model and we are not overwriting this default behavior in any of our models.
class CaseStudy(models.Model):

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = _('created by'), editable = False,
        null = True, on_delete = models.SET_NULL)
    name = models.CharField(verbose_name = _("case study name"), max_length = 150)
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    number_of_pests = models.IntegerField(verbose_name = _("number of pests"))
    number_of_hosts = models.IntegerField(verbose_name = _("number of hosts"))
    # all_plants = models.FilePathField(verbose_name = _("all plants"), path=settings.FILE_PATH_FIELD_DIRECTORY, match=None, recursive=False, max_length=200, null = True)
    start_year = models.DateField(verbose_name = _("start year"), auto_now=False, auto_now_add=False)
    end_year = models.DateField(verbose_name = _("end year"), auto_now=False, auto_now_add=False)
    # directory_name =os.path.join(settings.FILE_PATH_FIELD_DIRECTORY, CaseStudy.name)
    infestation_data = models.FileField(verbose_name = _("infestation data"), upload_to=settings.FILE_PATH_FIELD_DIRECTORY, max_length=100)
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    TIME_STEP_CHOICES = ((MONTH, 'Month'), (WEEK, 'Week'), (DAY, 'Day'))
    time_step = models.CharField(verbose_name = _("time step"), max_length = 50, choices = TIME_STEP_CHOICES)

    class Meta:
        verbose_name = _("case study")
        verbose_name_plural = _("case studies")

    def __str__(self):
        return self.name

class Host(models.Model):

    case_study = models.ManyToManyField(CaseStudy, verbose_name = _("case study"))
    name = models.CharField(verbose_name = _("host common name"), max_length = 150)
    score = models.IntegerField(verbose_name = _("score"))
    # host_data = models.FilePathField(verbose_name = _("host data"), path=settings.FILE_PATH_FIELD_DIRECTORY, match=None, recursive=True, max_length=100)

    class Meta:
        verbose_name = _("host")
        verbose_name_plural = _("hosts")

    def __str__(self):
        return self.name

class Mortality(models.Model):

    host = models.ForeignKey(Host, verbose_name = _("host"), on_delete = models.CASCADE)
    user_input = models.BooleanField(verbose_name = _("user inputs the mortality rate and time lag"), default = False)
    rate = models.FloatField(verbose_name = _("mortality rate"))
    rate_standard_deviation = models.FloatField(verbose_name = _("mortality rate standard deviation"))
    time_lag = models.IntegerField(verbose_name = _("mortality time lag"))
    time_lag_standard_deviation = models.FloatField(verbose_name = _("mortality time lag standard deviation"))

    class Meta:
        verbose_name = _("mortality")
        verbose_name_plural = _("mortalities")

    def __str__(self):
        return self.rate

class Creation(models.Model):

    host = models.ForeignKey(Host, verbose_name = _("host"), on_delete = models.CASCADE)

    class Meta:
        verbose_name = _("creation of host map")
        verbose_name_plural = _("creation of host maps")

    def __str__(self):
        return self.name

class PestInformation(models.Model):

    common_name = models.CharField(verbose_name = _("pest common name"), max_length = 150)
    scientific_name = models.CharField(verbose_name = _("pest scientific name"), max_length = 150)
    about = models.TextField(verbose_name = _("about the pest"))
    risks = models.TextField(verbose_name = _("risks associated with the pest"))
    management_activity = models.TextField(verbose_name = _("management activities to control the pest"))
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    date_updated = models.DateTimeField(verbose_name = _("date updated"), auto_now = True, auto_now_add = False)

    class Meta:
        verbose_name = _("pest information")
        verbose_name_plural = _("pest informations")

    def __str__(self):
        return self.common_name

class Pest(models.Model):

    name = models.CharField(verbose_name = _("pest common name"), max_length = 150)
    case_study = models.ManyToManyField(CaseStudy, verbose_name = _("case study"))
    pest_information = models.ForeignKey(PestInformation, verbose_name = _("pest information"), on_delete = models.CASCADE)
    staff_approved = models.BooleanField(verbose_name = _("approved by staff"))
    vector_born = models.BooleanField(verbose_name = _("vector born"), default = False)
    MODEL_CHOICES = (
        ("SI", "Susceptible Infected"),
        ("SID", "Susceptible Infected Diseased"),
        ("SEID", "Susceptible Exposed Infected Diseased"),
    )
    model_type = models.CharField(verbose_name = _("model type"), max_length = 20,
                    choices = MODEL_CHOICES,
                    default = "SI",)
    DISPERSAL_CHOICES = (
        ("CAUCHY", "Cauchy"),
        ("DOUBLE SCALE CAUCHY", "Double Scale Cauchy"),
        ("EXPONENTIAL", "Exponential"),
        ("DOUBLE SCALE EXPONENTIAL", "Double Scale Exponential")
    )
    dispersal_type = models.CharField(verbose_name = _("dispersal type"), max_length = 70,
                    choices = DISPERSAL_CHOICES,
                    default = "CAUCHY",)

    class Meta:
        verbose_name = _("pest")
        verbose_name_plural = _("pests")

    def __str__(self):
        return self.name

class Vector(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    common_name = models.CharField(verbose_name = _("vector common name"), max_length = 150)
    scientific_name = models.CharField(verbose_name = _("vector scientific name"), max_length = 150)
    vector_to_host_transmission_rate = models.IntegerField(verbose_name = _("vector to host transmission rate"))
    host_to_vector_transmission_rate = models.IntegerField(verbose_name = _("host to vector transmission rate"))

    class Meta:
        verbose_name = _("vector")
        verbose_name_plural = _("vectors")

    def __str__(self):
        return self.common_name

class ShortDistance(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    scale = models.FloatField(verbose_name = _("short distance scale"))
    scale_standard_deviation = models.FloatField(verbose_name = _("short distance scale standard deviation"))
    percent_short_distance = models.FloatField(verbose_name = _("percentage of dispersal that is short distance"), default = 1)

    class Meta:
        verbose_name = _("short distance dispersal")
        verbose_name_plural = _("short distance dispersals")

    def __str__(self):
        return self.scale

class LongDistance(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    scale = models.FloatField(verbose_name = _("long distance scale"))
    scale_standard_deviation = models.FloatField(verbose_name = _("long distance scale standard deviation"))

    class Meta:
        verbose_name = _("long distance dispersal")
        verbose_name_plural = _("long distance dispersals")

    def __str__(self):
        return self.scale

class CrypticToInfected(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    rate = models.FloatField(verbose_name = _("cryptic to infected rate"))
    rate_standard_deviation = models.FloatField(verbose_name = _("cryptic to infected standard deviation"))

    class Meta:
        verbose_name = _("cryptic to infected")
        verbose_name_plural = _("cryptic to infecteds")

    def __str__(self):
        return self.rate

class InfectedToDiseased(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    rate = models.FloatField(verbose_name = _("infected to diseased rate"))
    rate_standard_deviation = models.FloatField(verbose_name = _("infected to diseased standard deviation"))

    class Meta:
        verbose_name = _("infected to diseased")
        verbose_name_plural = _("infected to diseaseds")

    def __str__(self):
        return self.rate

class Weather(models.Model):

    case_study = models.ForeignKey(CaseStudy, verbose_name = _("case study"), on_delete = models.CASCADE)
    wind_on = models.BooleanField(verbose_name = _("use wind"), default = False)
    seasonality_on = models.BooleanField(verbose_name = _("use seasonality"), default = False)
    lethal_temp_on = models.BooleanField(verbose_name = _("use lethal temp"), default = False)
    temp_on = models.BooleanField(verbose_name = _("use temp"), default = False)
    precipitation_on = models.BooleanField(verbose_name = _("use precipitation"), default = False)

    class Meta:
        verbose_name = _("weather")
        verbose_name_plural = _("weathers")

    def __str__(self):
        return self.wind_on

class Wind(models.Model):

    weather = models.ForeignKey(Weather, verbose_name = _("weather"), on_delete = models.CASCADE)
    DIRECTION_CHOICES = (
        ("NONE", "None"),
        ("N", "North"),
        ("NE", "Northeast"),
        ("E", "East"),
        ("SE", "Southeast"),
        ("S", "South"),
        ("SW", "Southwest"),
        ("W", "West"),
        ("NW", "Northwest"),
    )
    wind_direction = models.CharField(verbose_name = _("wind direction"), max_length = 30,
                    choices = DIRECTION_CHOICES,
                    default = "NONE",)
    kappa = models.IntegerField(verbose_name = _("wind strenth (kappa)"), default = 0)

    class Meta:
        verbose_name = _("wind")
        verbose_name_plural = _("winds")

    def __str__(self):
        return self.wind_direction

class Seasonality(models.Model):

    weather = models.ForeignKey(Weather, verbose_name = _("weather"), on_delete = models.CASCADE)
    first_month = models.IntegerField(verbose_name = _("first month of season"), default = 1)
    last_month = models.IntegerField(verbose_name = _("last month of season"), default = 12)

    class Meta:
        verbose_name = _("seasonality")
        verbose_name_plural = _("seasonalities")

    def __str__(self):
        return self.first_month

class LethalTemperature(models.Model):

    weather = models.ForeignKey(Weather, verbose_name = _("weather"), on_delete = models.CASCADE)
    month = models.IntegerField(verbose_name = _("month in which lethal temperature occurs"), default = 1)
    value = models.FloatField(verbose_name = _("last month of season"), default = 0)
    # lethal_temperature_data = models.FilePathField(verbose_name = _("lethal temperature data"), path=None, match=None, recursive=True, max_length=100)

    class Meta:
        verbose_name = _("lethal temperature")
        verbose_name_plural = _("lethal temperatures")

    def __str__(self):
        return self.value

class Temperature(models.Model):

    weather = models.ForeignKey(Weather, verbose_name = _("weather"), on_delete = models.CASCADE)
    METHOD_CHOICES = (
        ("RECLASS", "Reclass"),
        ("POLYNOMIAL", "Polynomial"),
    )
    method = models.CharField(verbose_name = _("temperature coefficient creation method"), max_length = 30,
                    choices = METHOD_CHOICES,
                    default = "RECLASS",)
    # temperature_data = models.FilePathField(verbose_name = _("temperature data"), path=None, match=None, recursive=True, max_length=100)

    class Meta:
        verbose_name = _("temperature")
        verbose_name_plural = _("temperatures")

    def __str__(self):
        return self.method

class Precipitation(models.Model):

    weather = models.ForeignKey(Weather, verbose_name = _("weather"), on_delete = models.CASCADE)
    METHOD_CHOICES = (
        ("RECLASS", "Reclass"),
        ("POLYNOMIAL", "Polynomial"),
    )
    method = models.CharField(verbose_name = _("temperature coefficient creation method"), max_length = 30,
                    choices = METHOD_CHOICES,
                    default = "RECLASS",)
    # precipitation_data = models.FilePathField(verbose_name = _("precipitation data"), path=None, match=None, recursive=True, max_length=100)

    class Meta:
        verbose_name = _("precipitation")
        verbose_name_plural = _("precipitations")

    def __str__(self):
        return self.method

class TemperatureReclass(models.Model):

    temperature = models.ForeignKey(Temperature, verbose_name = _("temperature"), on_delete = models.CASCADE)
    threshold = models.FloatField(verbose_name = _("temperature threshold"))
    # matrix = MatrixField(verbose_name = _("matrix"), datatype = 'float')

    class Meta:
        verbose_name = _("temperature reclass")
        verbose_name_plural = _("temperature reclasses")

    def __str__(self):
        return self.threshold

class PrecipitationReclass(models.Model):

    precipitation = models.ForeignKey(Precipitation, verbose_name = _("precipitation"), on_delete = models.CASCADE)
    threshold = models.FloatField(verbose_name = _("precipitation threshold"))
    # matrix = MatrixField(verbose_name = _("matrix"), datatype = 'float')

    class Meta:
        verbose_name = _("precipitation reclass")
        verbose_name_plural = _("precipitation reclasses")

    def __str__(self):
        return self.threshold

class TemperaturePolynomial(models.Model):

    temperature = models.ForeignKey(Temperature, verbose_name = _("temperature"), on_delete = models.CASCADE)
    DEGREE_CHOICES = (
        ("1", "One"),
        ("2", "Two"),
        ("3", "Three"),
    )
    degree = models.FloatField(verbose_name = _("temperature polynomial degree"), 
                    choices = DEGREE_CHOICES, default = "1")
    a0 = models.FloatField(verbose_name = _("a0"))
    a1 = models.FloatField(verbose_name = _("a1"))
    a2 = models.FloatField(verbose_name = _("a2"))
    a3 = models.FloatField(verbose_name = _("a3"))
    x1 = models.FloatField(verbose_name = _("x1"))
    x2 = models.FloatField(verbose_name = _("x2"))
    x3 = models.FloatField(verbose_name = _("x3"))

    class Meta:
        verbose_name = _("temperature polynomial")
        verbose_name_plural = _("temperature polynomials")

    def __str__(self):
        return self.a0

class PrecipitationPolynomial(models.Model):

    precipitation = models.ForeignKey(Precipitation, verbose_name = _("precipitation"), on_delete = models.CASCADE)
    DEGREE_CHOICES = (
        ("1", "One"),
        ("2", "Two"),
        ("3", "Three"),
    )
    degree = models.FloatField(verbose_name = _("temperature polynomial degree"), 
                    choices = DEGREE_CHOICES, default = "1")
    a0 = models.FloatField(verbose_name = _("a0"))
    a1 = models.FloatField(verbose_name = _("a1"))
    a2 = models.FloatField(verbose_name = _("a2"))
    a3 = models.FloatField(verbose_name = _("a3"))
    x1 = models.FloatField(verbose_name = _("x1"))
    x2 = models.FloatField(verbose_name = _("x2"))
    x3 = models.FloatField(verbose_name = _("x3"))

    class Meta:
        verbose_name = _("precipitation polynomial")
        verbose_name_plural = _("precipitation polynomials")

    def __str__(self):
        return self.a0

class Session(models.Model):

    case_study = models.ForeignKey(CaseStudy, verbose_name = _("case study"), on_delete = models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = _('created by'), editable = False,
        null = True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    name = models.CharField(verbose_name = _("session name"), max_length=150)

    class Meta:
        verbose_name = _("session")
        verbose_name_plural = _("sessions")

    def __str__(self):
        return self.name

class Run(models.Model):

    session = models.ForeignKey(Session, verbose_name = _("session id"), on_delete = models.CASCADE)
    name = models.CharField(verbose_name = _("run name"), max_length = 150)
    random_seed = models.IntegerField(verbose_name = _("random seed"), default = None, null = True)

    class Meta:
        verbose_name = _("run")
        verbose_name_plural = _("runs")

    def __str__(self):
        return self.name

class InputChange(models.Model):

    run = models.ForeignKey(Run, verbose_name = _("run id"), on_delete = models.CASCADE)
    name = models.CharField(verbose_name = _("parameter name"), max_length = 150)
    value = models.FloatField(verbose_name = _("parameter value"))

    class Meta:
        verbose_name = _("input change")
        verbose_name_plural = _("input changes")

    def __str__(self):
        return self.name

class Output(models.Model):

    run = models.ForeignKey(Run, verbose_name = _("run id"), on_delete = models.CASCADE)
    name = models.CharField(verbose_name = _("output variable name"), max_length = 150)
    # data = MatrixField(verbose_name = _("output data"), datatype = 'float')

    class Meta:
        verbose_name = _("output")
        verbose_name_plural = _("outputs")

    def __str__(self):
        return self.name
