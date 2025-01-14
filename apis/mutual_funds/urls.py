from django.urls import path, include

from .viewsets import  MutualFundViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("mutual-funds", MutualFundViewSet,basename="mutual_funds")


urlpatterns = [
    path("", include(router.urls)),
]
