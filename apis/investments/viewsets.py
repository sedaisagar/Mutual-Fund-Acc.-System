from rest_framework import viewsets, mixins
from rest_framework.response import Response
from apps.accountings.models import UserInvestments
from .serializers import (
    UserInvestmentsSerializer,
    UserInvestmentsListSerializer,
    UserReportSerializer,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from django.db.models import F


@extend_schema(tags=["User Investment (s)"])
class UserInvestmentsViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = UserInvestments.objects.all()
    serializer_class = UserInvestmentsSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        action = self.action
        if action == "list":
            return UserInvestmentsListSerializer
        return UserInvestmentsSerializer

    def get_queryset(self):
        """
        Filter investment data based on current context user
        """
        return super().get_queryset().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create new mutual fund object
        """
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        List all mutual fund object
        """
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Investment Report (s)"])
class ReportGenerateView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserInvestments.objects.all()
    serializer_class = UserReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        List all reports
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        queryset = queryset.annotate(
            mutual_fund_name=F("mutual_fund__name"),
            total_units=F("units"),
            total_value=F("units") * F("mutual_fund__nav"),
        ).values("mutual_fund_name", "total_units", "total_value")

        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "results": serializer.data,
            }
        )
