from django.contrib import admin

from .models import CaseStudy, Host, Mortality, PestInformation, Pest, Vector, ShortDistance, LongDistance, CrypticToInfected, InfectedToDiseased, Weather, Wind, Seasonality, LethalTemperature, Temperature, Precipitation, TemperatureReclass, PrecipitationReclass, TemperaturePolynomial, PrecipitationPolynomial, Session, Run, InputChange, Output

class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_pests', 'number_of_hosts', 'start_year', 'end_year', 'time_step', 'created_by', 'date_created')

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user

        return super(CaseStudyAdmin, self).save_model(request, obj, form, change)

class HostAdmin(admin.ModelAdmin):
    list_display = ('name','score')


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
admin.site.register(TemperatureReclass)
admin.site.register(TemperaturePolynomial)
admin.site.register(PrecipitationReclass)
admin.site.register(PrecipitationPolynomial)
admin.site.register(Session)
admin.site.register(Run)
admin.site.register(InputChange)
admin.site.register(Output)
