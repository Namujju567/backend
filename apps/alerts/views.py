from rest_framework import generics
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
        status = self.request.query_params.get('status', None)
        
        if severity:
            queryset = queryset.filter(severity=severity)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset


class AlertDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


@api_view(['GET'])
def alert_counts(request):
    high = Alert.objects.filter(severity='High', status='active', dismissed=False).count()
    medium = Alert.objects.filter(severity='Medium', status='active', dismissed=False).count()
    low = Alert.objects.filter(severity='Low', status='active', dismissed=False).count()
    return Response({'High': high, 'Medium': medium, 'Low': low})
