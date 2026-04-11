from rest_framework import serializers
from .models import SystemSettings, PowerDevice


class SystemSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SystemSettings
        fields = [
            'api_endpoint', 'api_key', 'poll_interval',
            'default_location', 'device_timeout', 'temperature_unit', 'auto_reconnect',
            'alert_email', 'low_threshold', 'email_alerts', 'sms_alerts', 'push_alerts',
            'system_online',
        ]


class PowerDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PowerDevice
        fields = ['id', 'name', 'group', 'status']
