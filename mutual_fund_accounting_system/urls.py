"""
URL configuration for mutual_fund_accounting_system project.

The `urlpatterns` list routes URLs to views.
"""

from django.urls import path, include
from .info import home_page

urlpatterns = [
    # Just Normal Landing Page
    path("", home_page),

    path(
        "api/",
        include("apis.urls"),
    ),  # All Api urls
]
