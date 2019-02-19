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
        fields = ['method','precipitationreclass_set','precipitationpolynomial','precipitation_data']

class TemperatureSerializer(serializers.ModelSerializer):
    temperaturereclass_set=TemperatureReclassSerializer(many=True)
    temperaturepolynomial=TemperaturePolynomialSerializer()
    class Meta:
        model = Temperature
        fields = ['method','temperaturereclass_set','temperaturepolynomial','temperature_data']
        
class LethalTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LethalTemperature
        fields = ('lethal_type','month','value','lethal_temperature_data')

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
        fields = ('pk','wind_on','seasonality_on','lethal_temp_on','temp_on','precipitation_on','wind','seasonality','lethaltemperature','temperature','precipitation')

class HostDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostData
        fields = ['user_file']

class MortalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mortality
        fields = ['method','user_file','rate','rate_standard_deviation','time_lag','time_lag_standard_deviation']

class HostSerializer(serializers.ModelSerializer):
    hostdata = HostDataSerializer()
    mortality = MortalitySerializer()
    class Meta:
        model = Host
        fields = ['pk','name','score','hostdata','mortality_on','mortality']

class InfectedToDiseasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfectedToDiseased
        fields = ['rate','rate_standard_deviation']

class CrypticToInfectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrypticToInfected
        fields = ['rate','rate_standard_deviation']

class LongDistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongDistance
        fields = ['scale','scale_standard_deviation']

class ShortDistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortDistance
        fields = ['scale','scale_standard_deviation','percent_short_distance']

class PestInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PestInformation
        fields = ['common_name']

class VectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vector
        fields = ['common_name','scientific_name','user_file','vector_to_host_transmission_rate','vector_to_host_transmission_rate_standard_deviation','host_to_vector_transmission_rate','host_to_vector_transmission_rate_standard_deviation']

class PriorTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorTreatment
        fields = ['user_file']

class InitialInfestationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitialInfestation
        fields = ['user_file']

class PestSerializer(serializers.ModelSerializer):
    pest_information = PestInformationSerializer()
    vector = VectorSerializer()
    initialinfestation = InitialInfestationSerializer()
    priortreatment = PriorTreatmentSerializer()
    shortdistance = ShortDistanceSerializer()
    longdistance = LongDistanceSerializer()
    cryptictoinfected = CrypticToInfectedSerializer()
    infectedtodiseased = InfectedToDiseasedSerializer()
    class Meta:
        model = Pest
        fields = ['pk','pest_information','name','model_type','dispersal_type','initialinfestation','vector_born','vector','use_treatment','priortreatment','shortdistance','longdistance','cryptictoinfected','infectedtodiseased']
        
class AllPlantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllPlantsData
        fields = ['user_file']

class CaseStudySerializer(serializers.ModelSerializer):
    allplantsdata = AllPlantsSerializer()
    weather = WeatherSerializer()
    pest_set = PestSerializer(many=True)
    host_set = HostSerializer(many=True)
    class Meta:
        model = CaseStudy
        fields = ['name', 'description','number_of_pests','number_of_hosts','start_year','end_year','future_years',
                'time_step','staff_approved','calibration_status','use_external_calibration','calibration','allplantsdata','pest_set','host_set','weather']



