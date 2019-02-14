#from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import *

class TemperaturePolynomialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperaturePolynomial
        fields = ['degree','a0','a1','a2','a3','x1','x2','x3']

class PrecipitationPolynomialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecipitationPolynomial
        fields = ['degree','a0','a1','a2','a3','x1','x2','x3']

class TemperatureReclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureReclass
        fields = ['min_value','max_value','reclass']

class PrecipitationReclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecipitationReclass
        fields = ['min_value','max_value','reclass']

class PrecipitationSerializer(serializers.ModelSerializer):
    precipitationreclass_set=PrecipitationReclassSerializer(many=True)
    precipitationpolynomial=PrecipitationPolynomialSerializer()
    class Meta:
        model = Precipitation
        fields = ['method','precipitationreclass_set','precipitationpolynomial']

class TemperatureSerializer(serializers.ModelSerializer):
    temperaturereclass_set=TemperatureReclassSerializer(many=True)
    temperaturepolynomial=TemperaturePolynomialSerializer()
    class Meta:
        model = Temperature
        fields = ['method','temperaturereclass_set','temperaturepolynomial']
        
class LethalTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LethalTemperature
        fields = ('lethal_type','month','value')

class SeasonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasonality
        fields = ('first_month','last_month')

class WindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wind
        fields = ('wind_direction','kappa')

class WeatherSerializer(serializers.ModelSerializer):
    wind = WindSerializer()
    seasonality = WindSerializer()
    lethaltemperature = LethalTemperatureSerializer()
    temperature = TemperatureSerializer()
    precipitation = PrecipitationSerializer()
    class Meta:
        model = Weather
        fields = ('wind_on','seasonality_on','lethal_temp_on','temp_on','precipitation_on','wind','seasonality','lethaltemperature','temperature','precipitation')

class CaseStudySerializer(serializers.ModelSerializer):
    weather = WeatherSerializer()
    class Meta:
        model = CaseStudy
        fields = ['name', 'description','number_of_pests','number_of_hosts','start_year','end_year','future_years',
                'time_step','infestation_data','all_plants','use_treatment','treatment_data','weather']



