from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import KPI, Sensor, Device, Alert
from .serializers import KPISerializer, SensorSerializer, DeviceSerializer, AlertSerializer


class KPIList(generics.ListAPIView):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer


class SensorList(generics.ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class DeviceList(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class AlertList(generics.ListAPIView):
    queryset = Alert.objects.order_by('-time')
    serializer_class = AlertSerializer


@api_view(['GET'])
def activity_waveform(request):
    hours = ['6am','7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm']
    values = [12, 28, 45, 62, 80, 95, 88, 74, 60, 48, 35, 20]
    return Response({'hours': hours, 'values': values})


@api_view(['GET'])
def dashboard_summary(request):
    active_alerts = Alert.objects.filter(severity='High', is_read=False).count()
    return Response({
        'readable_date': timezone.localtime().strftime('%A, %B %d, %Y'),
        'station': 'Main Entrance Station',
        'status': 'System Operational',
        'active_alerts': active_alerts,
    })

