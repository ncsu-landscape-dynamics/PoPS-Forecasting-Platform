from django.contrib import admin

from .models import CaseStudy, MapBoxParameters, AllPlantsData, Host, HostData, Mortality, MortalityRate, MortalityTimeLag, Creation, PestInformation, Pest, Vector, VectorHostTransmissionRate, VectorReproductiveRate, VectorNaturalDistance, HostVectorTransmissionRate, ReproductiveRate, PercentNaturalDistance,  NaturalDistance, AnthropogenicDistance, AnthropogenicDirection, CrypticToInfected, InfectedToDiseased, PriorTreatment, PriorTreatmentYear, Weather, Wind, Seasonality, LethalTemperature, Temperature, Precipitation, TemperatureReclass, PrecipitationReclass, TemperaturePolynomial, PrecipitationPolynomial, Session, Run, RunCollection, Output, CalibrationInfestation, ValidationInfestation, InitialInfestation

class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_pests', 'number_of_hosts', 'start_year', 'end_year', 'time_step', 'created_by', 'date_created')

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

        return super(CaseStudyAdmin, self).save_model(request, obj, form, change)

class HostAdmin(admin.ModelAdmin):
    list_display = ('name','score')

class TemperatureReclassAdmin(admin.ModelAdmin):
    list_display = ('__str__','min_value','max_value','reclass')

class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'case_study', 'date_created')

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

        return super(SessionAdmin, self).save_model(request, obj, form, change)

class RunCollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'session','date_created','status','tangible_landscape')

class RunAdmin(admin.ModelAdmin):
    list_display = ('run_collection', 'steering_year','date_created','status')
    
admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(AllPlantsData)
admin.site.register(HostData)
admin.site.register(Creation)
admin.site.register(PriorTreatment)
admin.site.register(PriorTreatmentYear)
admin.site.register(Mortality)
admin.site.register(MortalityRate)
admin.site.register(MortalityTimeLag)
admin.site.register(PestInformation)
admin.site.register(Pest)
admin.site.register(Vector)
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
admin.site.register(Weather)
admin.site.register(Wind)
admin.site.register(Seasonality)
admin.site.register(LethalTemperature)
admin.site.register(Temperature)
admin.site.register(Precipitation)
admin.site.register(TemperatureReclass,TemperatureReclassAdmin)
admin.site.register(TemperaturePolynomial)
admin.site.register(PrecipitationReclass)
admin.site.register(PrecipitationPolynomial)
admin.site.register(Session,SessionAdmin)
admin.site.register(Run,RunAdmin)
admin.site.register(RunCollection,RunCollectionAdmin)
admin.site.register(Output)
admin.site.register(CalibrationInfestation)
admin.site.register(ValidationInfestation)
admin.site.register(InitialInfestation)

