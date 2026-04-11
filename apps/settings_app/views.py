from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .models import SystemSettings, PowerDevice
from .serializers import SystemSettingsSerializer, PowerDeviceSerializer
from apps.alerts.utils import create_alert


@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH'])
def settings_view(request):
    obj = SystemSettings.get()
    if request.method == 'GET':
        return Response(SystemSettingsSerializer(obj).data)

    serializer = SystemSettingsSerializer(obj, data=request.data, partial=request.method == 'PATCH')
    if serializer.is_valid():
        serializer.save()
        create_alert(
            title    = 'System Settings Updated',
            device   = 'Dashboard',
            message  = 'System settings were saved from the Settings page.',
            severity = 'Low',
            location = 'Dashboard',
        )
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PATCH'])
def system_power_view(request):
    obj = SystemSettings.get()
    if request.method == 'GET':
        return Response({'system_online': obj.system_online})

    new_state = request.data.get('system_online')
    if new_state is None:
        return Response({'error': 'system_online required.'}, status=status.HTTP_400_BAD_REQUEST)

    obj.system_online = new_state
    obj.save(update_fields=['system_online'])

    create_alert(
        title    = 'System Powered On' if new_state else 'System Powered Off',
        device   = 'Dashboard',
        message  = f'System was remotely {"activated" if new_state else "shut down"} from Settings.',
        severity = 'Low' if new_state else 'High',
        location = 'Settings',
    )
    return Response({'system_online': obj.system_online})


@csrf_exempt
@api_view(['GET'])
def power_devices_list(request):
    qs = PowerDevice.objects.all()
    return Response(PowerDeviceSerializer(qs, many=True).data)


@csrf_exempt
@api_view(['PATCH'])
def power_device_toggle(request, pk):
    try:
        device = PowerDevice.objects.get(pk=pk)
    except PowerDevice.DoesNotExist:
        return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    old_status = device.status
    device.status = request.data.get('status', device.status)
    device.save()

    if device.status != old_status:
        if device.status:
            create_alert(
                title    = 'Device Powered On',
                device   = device.name,
                message  = f'{device.name} was powered on from the Settings panel.',
                severity = 'Low',
                location = 'Settings',
                status   = 'resolved',
            )
        else:
            create_alert(
                title    = 'Device Powered Off',
                device   = device.name,
                message  = f'{device.name} was powered off from the Settings panel.',
                severity = 'Medium',
                location = 'Settings',
            )

    return Response(PowerDeviceSerializer(device).data)
