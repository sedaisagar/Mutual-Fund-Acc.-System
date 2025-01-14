from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.urls import path

urlpatterns = [
    path("", SpectacularSwaggerView.as_view()),
    path("redoc", SpectacularRedocView.as_view()),
    path("schema", SpectacularAPIView.as_view(), name='schema'),
]
