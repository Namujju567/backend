from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.settings_view,       name='settings'),
    path('system-power/',       views.system_power_view,   name='system-power'),
    path('power/',              views.power_devices_list,  name='power-list'),
    path('power/<int:pk>/',     views.power_device_toggle, name='power-toggle'),
]
