from rest_framework import viewsets
from rest_framework import permissions
from django.db.models import Prefetch


from ..models import *
from ..serializers import *

class CaseStudyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows case studies to be viewed or edited.
    """
    queryset = CaseStudy.objects.prefetch_related(
        Prefetch('host_set', queryset=Host.objects.select_related('mortality','hostdata')),
        Prefetch('pest_set',queryset=Pest.objects.select_related('vector','initialinfestation',
        'priortreatment','shortdistance','longdistance','cryptictoinfected','infectedtodiseased')),
        Prefetch('weather__temperature__temperaturereclass_set'),
        Prefetch('weather__precipitation__precipitationreclass_set')).select_related(
            'created_by','allplantsdata','weather__wind','weather__seasonality',
            'weather__lethaltemperature','weather__temperature','weather__temperature__temperaturepolynomial',
            'weather__precipitation', 'weather__precipitation__precipitationpolynomial').all()
    serializer_class = CaseStudySerializer
    permission_classes = (permissions.AllowAny,)

class RunViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows runs to be viewed or edited.
    """
    queryset = Run.objects.prefetch_related().all()
    serializer_class = RunSerializer
    permission_classes = (permissions.AllowAny,)


class OutputViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows output to be viewed or edited.
    """
    queryset = Output.objects.prefetch_related().all()
    serializer_class = OutputSerializer
    permission_classes = (permissions.AllowAny,)

class TemperatureDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows output to be viewed or edited.
    """
    queryset = Temperature.objects.prefetch_related().all()
    serializer_class = TemperatureDataSerializer
    permission_classes = (permissions.AllowAny,)

class LethalTemperatureDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows output to be viewed or edited.
    """
    queryset = LethalTemperature.objects.prefetch_related().all()
    serializer_class = LethalTemperatureDataSerializer
    permission_classes = (permissions.AllowAny,)

class PrecipitationDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows output to be viewed or edited.
    """
    queryset = Precipitation.objects.prefetch_related().all()
    serializer_class = PrecipitationDataSerializer
    permission_classes = (permissions.AllowAny,)