from django.contrib import admin

from .models import CaseStudy, Host, Mortality, PestInformation, Pest, Vector, ShortDistance, LongDistance, CrypticToInfected, InfectedToDiseased, Weather, Wind, Seasonality, LethalTemperature, Temperature, Precipitation, TemperatureReclass, PrecipitationReclass, TemperaturePolynomial, PrecipitationPolynomial, Session, Run, Output, CalibrationInfestation, ValidationInfestation, InitialInfestation

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

admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Mortality)
admin.site.register(PestInformation)
admin.site.register(Pest)
admin.site.register(Vector)
admin.site.register(ShortDistance)
admin.site.register(LongDistance)
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
admin.site.register(Run)
admin.site.register(Output)
admin.site.register(CalibrationInfestation)
admin.site.register(ValidationInfestation)
admin.site.register(InitialInfestation)

