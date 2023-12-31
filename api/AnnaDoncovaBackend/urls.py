"""
URL configuration for AnnaDoncovaBackend project.

The `urlpatterns` list routes URLs to views.
"""
from django.urls import include, path

urlpatterns = [
    path('api/', include('app.urls'))
]
