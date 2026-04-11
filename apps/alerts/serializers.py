from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'title', 'device', 'location', 'message', 'time', 'date', 'severity', 'status', 'dismissed']
