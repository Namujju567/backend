from django.contrib import admin
from .models import SensorReading


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('date', 'device', 'soap_usage', 'water_usage', 'handwashes', 'unwashed')
    list_filter = ('device',)
    date_hierarchy = 'date'
