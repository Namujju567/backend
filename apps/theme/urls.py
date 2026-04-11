from django.urls import path
from .views import theme_view

urlpatterns = [
    path('', theme_view, name='theme_view'),
]
