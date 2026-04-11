from django.urls import path
from . import views

urlpatterns = [
    path('kpi/', views.KPIList.as_view(), name='dashboard-kpi'),
    path('sensors/', views.SensorList.as_view(), name='dashboard-sensors'),
    path('devices/', views.DeviceList.as_view(), name='dashboard-devices'),
    path('alerts/', views.AlertList.as_view(), name='dashboard-alerts'),
    path('activity/', views.activity_waveform, name='dashboard-activity'),
    path('summary/', views.dashboard_summary, name='dashboard-summary'),
]
