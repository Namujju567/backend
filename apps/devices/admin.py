from django.contrib import admin
from .models import Device, DeviceSensorReading


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display  = ('name', 'location', 'status', 'battery', 'wired', 'last_active')
    list_filter   = ('status', 'location')
    search_fields = ('name', 'location')


@admin.register(DeviceSensorReading)
class DeviceSensorReadingAdmin(admin.ModelAdmin):
    list_display = ('device', 'timestamp', 'water_level', 'soap_level', 'temperature', 'value')
    list_filter  = ('device',)
