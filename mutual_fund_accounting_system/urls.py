"""
URL configuration for mutual_fund_accounting_system project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/",include("apis.urls"),)
]
