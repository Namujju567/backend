from django.contrib import admin
from .models import SystemSettings, PowerDevice


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('api_endpoint', 'default_location', 'temperature_unit', 'auto_reconnect')


@admin.register(PowerDevice)
class PowerDeviceAdmin(admin.ModelAdmin):
    list_display  = ('name', 'group', 'status')
    list_filter   = ('group', 'status')
    list_editable = ('status',)
