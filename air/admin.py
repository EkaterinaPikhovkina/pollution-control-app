from django.contrib import admin

from .models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class PollutantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'norm_ind')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'kind')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'kind')
    list_filter = ('kind',)


class AirDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime', 'city', 'pollutant', 'concentration', 'sensor', 'author')
    list_display_links = ('id', 'city', 'pollutant', 'sensor', 'author')
    search_fields = ('datetime', 'city', 'pollutant', 'sensor', 'author')
    list_filter = ('datetime', 'city', 'pollutant', 'concentration', 'sensor', 'author')


class PreventionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    list_display_links = ('id',)
    search_fields = ('description',)
    list_editable = ('description',)


class AdviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'pollutant', 'prevention')
    list_display_links = ('id', 'pollutant')
    search_fields = ('pollutant', 'prevention')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime', 'advice')
    list_display_links = ('id',)
    search_fields = ('datetime', 'advice')
    list_filter = ('datetime',)


admin.site.register(City, CityAdmin)
admin.site.register(Pollutant, PollutantAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(AirData, AirDataAdmin)
admin.site.register(Prevention, PreventionAdmin)
admin.site.register(Advice, AdviceAdmin)
admin.site.register(News, NewsAdmin)
