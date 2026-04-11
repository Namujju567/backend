from datetime import date, timedelta
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import SensorReading
from .serializers import SensorReadingSerializer
from apps.alerts.utils import create_alert


def _aggregate(qs):
    """Turn a queryset of SensorReadings into the chart-ready dict."""
    labels, soap, water, washed, unwashed = [], [], [], [], []
    for r in qs:
        labels.append(r.date.strftime('%b %d').replace(' 0', ' ') if hasattr(r.date, 'strftime') else str(r.date))
        soap.append(round(r.soap_usage, 2))
        water.append(round(r.water_usage, 2))
        washed.append(r.handwashes)
        unwashed.append(r.unwashed)
    return {
        'labels': labels,
        'soapUsage': soap,
        'waterUsage': water,
        'handwashes': washed,
        'unwashed': unwashed,
    }


@api_view(['GET'])
def analytics_week(request):
    today = date.today()
    start = today - timedelta(days=6)
    qs = SensorReading.objects.filter(date__range=(start, today))
    return Response(_aggregate(qs))


@api_view(['GET'])
def analytics_month(request):
    today = date.today()
    start = date(today.year, 1, 1)
    from django.db.models.functions import TruncMonth
    from django.db.models import Avg

    rows = (
        SensorReading.objects
        .filter(date__range=(start, today))
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(
            soap_usage=Sum('soap_usage'),
            water_usage=Sum('water_usage'),
            handwashes=Sum('handwashes'),
            unwashed=Sum('unwashed'),
        )
        .order_by('month')
    )

    labels, soap, water, washed, unw = [], [], [], [], []
    for r in rows:
        labels.append(r['month'].strftime('%b'))
        soap.append(round(r['soap_usage'] or 0, 2))
        water.append(round(r['water_usage'] or 0, 2))
        washed.append(r['handwashes'] or 0)
        unw.append(r['unwashed'] or 0)

    return Response({
        'labels': labels,
        'soapUsage': soap,
        'waterUsage': water,
        'handwashes': washed,
        'unwashed': unw,
    })


@api_view(['GET'])
def analytics_range(request):
    from_date = request.query_params.get('from')
    to_date = request.query_params.get('to')
    if not from_date or not to_date:
        return Response({'error': 'from and to query params required.'}, status=status.HTTP_400_BAD_REQUEST)
    qs = SensorReading.objects.filter(date__range=(from_date, to_date))
    return Response(_aggregate(qs))


@api_view(['POST'])
def iot_ingest(request):
    """
    IoT devices POST readings here.
    Expected payload:
    {
        "date": "2025-07-20",
        "device": "IoT-Station-01",
        "soap_usage": 1.8,
        "water_usage": 145.0,
        "handwashes": 62,
        "unwashed": 8
    }
    """
    serializer = SensorReadingSerializer(data=request.data)
    if serializer.is_valid():
        obj, created = SensorReading.objects.update_or_create(
            date=serializer.validated_data['date'],
            device=serializer.validated_data['device'],
            defaults={
                'soap_usage': serializer.validated_data['soap_usage'],
                'water_usage': serializer.validated_data['water_usage'],
                'handwashes': serializer.validated_data['handwashes'],
                'unwashed': serializer.validated_data['unwashed'],
            }
        )

        soap  = serializer.validated_data['soap_usage']
        water = serializer.validated_data['water_usage']
        unwashed = serializer.validated_data['unwashed']
        device_name = serializer.validated_data['device']

        if soap < 0.3:
            create_alert(
                title    = 'Critical Soap Supply',
                device   = device_name,
                message  = f'Daily soap usage dropped to {soap}L — dispenser may be empty.',
                severity = 'High',
            )
        if water < 10:
            create_alert(
                title    = 'Low Water Usage Detected',
                device   = device_name,
                message  = f'Water usage is only {water}L today — possible supply issue.',
                severity = 'Medium',
            )
        if unwashed > 50:
            create_alert(
                title    = 'High Non-Compliance Rate',
                device   = device_name,
                message  = f'{unwashed} people left without washing hands today.',
                severity = 'High',
            )

        return Response(SensorReadingSerializer(obj).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
