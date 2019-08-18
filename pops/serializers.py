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

class TemperatureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = '__all__'

class WeatherSerializer(serializers.ModelSerializer):
    wind = WindSerializer()
    seasonality = SeasonalitySerializer()
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
        fields = ['pk','value','probability']

class CrypticToInfectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrypticToInfected
        fields = ['pk','value','probability']

class AnthropogenicDistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnthropogenicDistance
        fields = ['pk','value','probability']

class NaturalDistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaturalDistance
        fields = ['pk','value','probability']

class PercentNaturalDistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentNaturalDistance
        fields = ['pk','value','probability']

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
    naturaldistance_set = NaturalDistanceSerializer(many=True)
    anthropogenicdistance_set = AnthropogenicDistanceSerializer(many=True)
    percentnaturaldistance_set = PercentNaturalDistanceSerializer(many=True)
    cryptictoinfected_set = CrypticToInfectedSerializer(many=True)
    infectedtodiseased_set = InfectedToDiseasedSerializer(many=True)
    class Meta:
        model = Pest
        fields = ['pk','pest_information','name','model_type','natural_dispersal_type', 'anthropogenic_dispersal_type','initialinfestation','vector_born','vector','use_treatment','priortreatment','naturaldistance_set','anthropogenicdistance_set','percentnaturaldistance_set','cryptictoinfected_set','infectedtodiseased_set']
        
class AllPlantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllPlantsData
        fields = ['user_file']

class MapBoxParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapBoxParameters
        fields = ['longitude', 'latitude','zoom']

class CaseStudySerializer(serializers.ModelSerializer):
    allplantsdata = AllPlantsSerializer()
    mapboxparameters = MapBoxParametersSerializer()
    weather = WeatherSerializer()
    pest_set = PestSerializer(many=True)
    host_set = HostSerializer(many=True)
    class Meta:
        model = CaseStudy
        fields = ['name', 'description','number_of_pests','number_of_hosts','start_year','end_year','future_years',
                'time_step','staff_approved','calibration_status','use_external_calibration','calibration','model_api','allplantsdata','mapboxparameters', 'pest_set','host_set','weather']

class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = '__all__'

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = '__all__'

class RunCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunCollection
        fields = '__all__'

class TemperatureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = '__all__'

class LethalTemperatureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LethalTemperature
        fields = '__all__'

class PrecipitationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precipitation
        fields = '__all__'

"""
class SessionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

    run_count = serializers.SerializerMethodField()
    most_recent_run = serializers.SerializerMethodField()

    def get_run_count(self, obj):
        return obj.run_set.count()

    def get_most_recent_run(self, obj):
        if obj.run_set.exists():
            return obj.run_set.order_by('-pk')[0].pk
        else:
            return 'null'
"""



