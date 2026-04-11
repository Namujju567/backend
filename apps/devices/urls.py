from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.DeviceList.as_view(),  name='device-list'),
    path('<int:pk>/',                 views.DeviceDetail.as_view(), name='device-detail'),
    path('<int:device_id>/ingest/',   views.iot_ingest,             name='device-ingest'),
    path('<int:device_id>/status/',   views.update_status,          name='device-status'),
]
