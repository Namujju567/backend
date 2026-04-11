from rest_framework import serializers
from .models import KPI, Sensor, Device, Alert


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ['id', 'label', 'value', 'change', 'up', 'color']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'label', 'value', 'pct', 'color', 'is_active']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'status', 'battery', 'color', 'location']


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'title', 'device', 'time', 'severity', 'is_read']
