from django.contrib import admin

from .models import *

class HostInline(admin.TabularInline):
    model = Host
    extra = 0
    show_change_link = True

class PestInline(admin.TabularInline):
    model = Pest
    extra = 0
    show_change_link = True

class HistoricDataInline(admin.TabularInline):
    model = HistoricData
    extra = 0
    show_change_link = True

class MapBoxParametersInline(admin.TabularInline):
    model = MapBoxParameters
    extra = 0
    show_change_link = True

class AllPlantsDataInline(admin.TabularInline):
    model = AllPlantsData
    extra = 0
    show_change_link = True

class HostDataInline(admin.TabularInline):
    model = HostData
    extra = 0
    show_change_link = True

class MortalityInline(admin.TabularInline):
    model = Mortality
    extra = 0
    show_change_link = True

class MortalityRateInline(admin.TabularInline):
    model = MortalityRate
    extra = 0
    show_change_link = True

class MortalityTimeLagInline(admin.TabularInline):
    model = MortalityTimeLag
    extra = 0
    show_change_link = True

class CreationInline(admin.TabularInline):
    model = Creation
    extra = 0
    show_change_link = True

class InitialInfestationInline(admin.TabularInline):
    model = InitialInfestation
    extra = 0
    show_change_link = True

class CalibrationInfestationInline(admin.TabularInline):
    model = CalibrationInfestation
    extra = 0
    show_change_link = True

class ValidationInfestationInline(admin.TabularInline):
    model = ValidationInfestation
    extra = 0
    show_change_link = True

class PriorTreatmentInline(admin.TabularInline):
    model = PriorTreatment
    extra = 0
    show_change_link = True

class PriorTreatmentYearInline(admin.TabularInline):
    model = PriorTreatmentYear
    extra = 0
    show_change_link = True

class VectorInline(admin.TabularInline):
    model = Vector
    extra = 0
    show_change_link = True

class ReproductiveRateInline(admin.TabularInline):
    model = ReproductiveRate
    extra = 0
    show_change_link = True

class PercentNaturalDistanceInline(admin.TabularInline):
    model = PercentNaturalDistance
    extra = 0
    show_change_link = True

class VectorHostTransmissionRateInline(admin.TabularInline):
    model = VectorHostTransmissionRate
    extra = 0
    show_change_link = True

class HostVectorTransmissionRateInline(admin.TabularInline):
    model = HostVectorTransmissionRate
    extra = 0
    show_change_link = True

class VectorReproductiveRateInline(admin.TabularInline):
    model = VectorReproductiveRate
    extra = 0
    show_change_link = True

class VectorNaturalDistanceInline(admin.TabularInline):
    model = VectorNaturalDistance
    extra = 0
    show_change_link = True

class NaturalDistanceInline(admin.TabularInline):
    model = NaturalDistance
    extra = 0
    show_change_link = True

class AnthropogenicDistanceInline(admin.TabularInline):
    model = AnthropogenicDistance
    extra = 0
    show_change_link = True

class AnthropogenicDirectionInline(admin.TabularInline):
    model = AnthropogenicDirection
    extra = 0
    show_change_link = True

class CrypticToInfectedInline(admin.TabularInline):
    model = CrypticToInfected
    extra = 0
    show_change_link = True

class InfectedToDiseasedInline(admin.TabularInline):
    model = InfectedToDiseased
    extra = 0
    show_change_link = True

class WeatherInline(admin.TabularInline):
    model = Weather
    extra = 0
    show_change_link = True

class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'session_count','start_year', 'end_year', 'time_step', 'created_by', 'date_created', 'model_api')
    inlines = [
        HostInline, PestInline, AllPlantsDataInline, HistoricDataInline, MapBoxParametersInline, WeatherInline
    ]
    search_fields = ['name','created_by__username','created_by__first_name','created_by__last_name', 'pest__name']
    list_select_related = ('created_by',)
    list_filter = ('staff_approved',)
    list_per_page = 30

    
    def session_count(self, obj):
        return obj.session_set.count()

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

        return super(CaseStudyAdmin, self).save_model(request, obj, form, change)

class HostAdmin(admin.ModelAdmin):
    list_display = ('name','score')
    inlines = [
        MortalityInline, CreationInline, HostDataInline
    ]

class PestAdmin(admin.ModelAdmin):
    list_display = ('__str__','name','pest_information')
    inlines = [
        InitialInfestationInline, CalibrationInfestationInline, ValidationInfestationInline, 
        PriorTreatmentInline, VectorInline, ReproductiveRateInline, PercentNaturalDistanceInline,
        NaturalDistanceInline, AnthropogenicDistanceInline, AnthropogenicDirectionInline,
        CrypticToInfectedInline, InfectedToDiseasedInline
    ]
    list_per_page = 30


class PriorTreatmentAdmin(admin.ModelAdmin):
    inlines = [
        PriorTreatmentYearInline
    ]

class VectorAdmin(admin.ModelAdmin):
    inlines = [
        VectorHostTransmissionRateInline, HostVectorTransmissionRateInline, VectorNaturalDistanceInline, VectorReproductiveRateInline
    ]

class TemperatureReclassAdmin(admin.ModelAdmin):
    list_display = ('__str__','min_value','max_value','reclass')

class PrecipitationReclassAdmin(admin.ModelAdmin):
    list_display = ('__str__','min_value','max_value','reclass')

class TemperatureReclassInline(admin.TabularInline):
    model = TemperatureReclass
    extra = 0
    show_change_link = True

class TemperaturePolynomialInline(admin.TabularInline):
    model = TemperaturePolynomial
    extra = 0
    show_change_link = True

class TemperatureAdmin(admin.ModelAdmin):
    inlines = [
        TemperatureReclassInline, TemperaturePolynomialInline
    ]

class PrecipitationReclassInline(admin.TabularInline):
    model = PrecipitationReclass
    extra = 0
    show_change_link = True

class PrecipitationPolynomialInline(admin.TabularInline):
    model = PrecipitationPolynomial
    extra = 0
    show_change_link = True

class PrecipitationAdmin(admin.ModelAdmin):
    inlines = [
        PrecipitationReclassInline, PrecipitationPolynomialInline
    ]

class WindInline(admin.TabularInline):
    model = Wind
    extra = 0
    show_change_link = True

class SeasonalityInline(admin.TabularInline):
    model = Seasonality
    extra = 0
    show_change_link = True

class TemperatureInline(admin.TabularInline):
    model = Temperature
    extra = 0
    show_change_link = True

class PrecipitationInline(admin.TabularInline):
    model = Precipitation
    extra = 0
    show_change_link = True

class LethalTemperatureInline(admin.TabularInline):
    model = LethalTemperature
    extra = 0
    show_change_link = True

class WeatherAdmin(admin.ModelAdmin):
    inlines = [
        WindInline, LethalTemperatureInline, SeasonalityInline, TemperatureInline, PrecipitationInline
    ]
    list_per_page = 30


class RunCollectionInline(admin.TabularInline):
    model = RunCollection
    extra = 0
    show_change_link = True

class AllowedUsersInline(admin.TabularInline):
    model = AllowedUsers
    extra = 0
    show_change_link = True

class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'run_collection_count','created_by', 'case_study', 'date_created')
    search_fields = ['name','created_by__username','created_by__first_name','created_by__last_name', 'case_study__name']
    list_select_related = ('created_by', 'case_study')
    list_filter = ['public','case_study']
    list_per_page = 30
    inlines = [
        RunCollectionInline,
        AllowedUsersInline
    ]

    def run_collection_count(self, obj):
        return obj.runcollection_set.count()

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

        return super(SessionAdmin, self).save_model(request, obj, form, change)


class RunInline(admin.TabularInline):
    model = Run
    extra = 0
    show_change_link = True

class RunCollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'session','date_created','status','tangible_landscape')
    inlines = [
        RunInline,
    ]
    list_per_page = 30


class OutputInline(admin.TabularInline):
    model = Output
    extra = 0
    show_change_link = True

class RunAdmin(admin.ModelAdmin):
    list_display = ('run_collection', 'steering_year','date_created','status')
    inlines = [
        OutputInline,
    ]
    list_per_page = 30


class AllowedUsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'session')
    list_per_page = 30

class SpreadRateInline(admin.TabularInline):
    model = SpreadRate
    show_change_link = True
    extra = 0

class DistanceToBoundaryInline(admin.TabularInline):
    model = DistanceToBoundary
    show_change_link = True
    extra = 0

class TimeToBoundaryInline(admin.TabularInline):
    model = TimeToBoundary
    show_change_link = True
    extra = 0

class OutputAdmin(admin.ModelAdmin):
    fields = ['run', 'number_infected']
    inlines = [
        SpreadRateInline, DistanceToBoundaryInline, TimeToBoundaryInline
    ]

admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(AllPlantsData)
admin.site.register(HostData)
admin.site.register(Creation)
admin.site.register(PriorTreatment, PriorTreatmentAdmin)
admin.site.register(PriorTreatmentYear)
admin.site.register(Mortality)
admin.site.register(MortalityRate)
admin.site.register(MortalityTimeLag)
admin.site.register(PestInformation)
admin.site.register(Pest, PestAdmin)
admin.site.register(Vector, VectorAdmin)
admin.site.register(VectorHostTransmissionRate)
admin.site.register(VectorReproductiveRate)
admin.site.register(VectorNaturalDistance)
admin.site.register(HostVectorTransmissionRate)
admin.site.register(ReproductiveRate)
admin.site.register(PercentNaturalDistance)
admin.site.register(NaturalDistance)
admin.site.register(AnthropogenicDistance)
admin.site.register(AnthropogenicDirection)
admin.site.register(CrypticToInfected)
admin.site.register(InfectedToDiseased)
admin.site.register(Weather, WeatherAdmin)
admin.site.register(Wind)
admin.site.register(Seasonality)
admin.site.register(LethalTemperature)
admin.site.register(Temperature, TemperatureAdmin)
admin.site.register(Precipitation, PrecipitationAdmin)
admin.site.register(TemperatureReclass,TemperatureReclassAdmin)
admin.site.register(TemperaturePolynomial)
admin.site.register(PrecipitationReclass, PrecipitationReclassAdmin)
admin.site.register(PrecipitationPolynomial)
admin.site.register(Session,SessionAdmin)
admin.site.register(Run,RunAdmin)
admin.site.register(RunCollection,RunCollectionAdmin)
admin.site.register(Output, OutputAdmin)
admin.site.register(CalibrationInfestation)
admin.site.register(ValidationInfestation)
admin.site.register(InitialInfestation)
admin.site.register(HistoricData)
admin.site.register(MapBoxParameters)
admin.site.register(AllowedUsers, AllowedUsersAdmin)
admin.site.register(SpreadRate)
admin.site.register(DistanceToBoundary)
admin.site.register(TimeToBoundary)
