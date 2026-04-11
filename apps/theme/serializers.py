from rest_framework import serializers
from .models import ThemePreference


class ThemePreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemePreference
        fields = ['theme']
