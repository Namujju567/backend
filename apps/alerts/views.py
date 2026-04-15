from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Alert
from .serializers import AlertSerializer


class AlertList(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def get_queryset(self):
        queryset = Alert.objects.filter(dismissed=False)
        severity = self.request.query_params.get('severity', None)
        status_param = self.request.query_params.get('status', None)
        if severity:
            queryset = queryset.filter(severity=severity)
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset


class AlertDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


@api_view(['PATCH'])
def mark_read(request, pk):
    try:
        alert = Alert.objects.get(pk=pk)
    except Alert.DoesNotExist:
        return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    alert.dismissed = True
    alert.save(update_fields=['dismissed'])
    return Response({'ok': True})


@api_view(['PATCH'])
def mark_all_read(request):
    Alert.objects.filter(dismissed=False, status='active').update(dismissed=True)
    return Response({'ok': True})


@api_view(['GET'])
def alert_counts(request):
    high   = Alert.objects.filter(severity='High',   status='active', dismissed=False).count()
    medium = Alert.objects.filter(severity='Medium', status='active', dismissed=False).count()
    low    = Alert.objects.filter(severity='Low',    status='active', dismissed=False).count()
    return Response({'High': high, 'Medium': medium, 'Low': low})
