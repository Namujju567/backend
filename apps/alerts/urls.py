from django.urls import path
from . import views

urlpatterns = [
    path('',                views.AlertList.as_view(), name='alert-list'),
    path('<int:pk>/',       views.AlertDetail.as_view(), name='alert-detail'),
    path('<int:pk>/read/',  views.mark_read,            name='alert-read'),
    path('read-all/',       views.mark_all_read,        name='alert-read-all'),
    path('counts/',         views.alert_counts,         name='alert-counts'),
]
