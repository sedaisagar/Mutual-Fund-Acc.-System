from django.urls import path, include

from .viewsets import UserInvestmentsViewSet,ReportGenerateView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("investments", UserInvestmentsViewSet, basename="user_investments")
router.register("report", ReportGenerateView, basename="user_investment_reports")


urlpatterns = [
    path("", include(router.urls)),
]
