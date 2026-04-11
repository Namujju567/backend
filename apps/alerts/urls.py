from django.urls import path
from . import views

urlpatterns = [
    path('', views.AlertList.as_view(), name='alert-list'),
    path('<int:pk>/', views.AlertDetail.as_view(), name='alert-detail'),
    path('counts/', views.alert_counts, name='alert-counts'),
]
