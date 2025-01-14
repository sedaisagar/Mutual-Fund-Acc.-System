from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from apps.accountings.models import MutualFunds
from .serializers import MutualFundsSerializer, MutualFundsUpdateSerializer,MutualFundsGetSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser, AllowAny


@extend_schema(tags=["Mutual Fund (s)"])
class MutualFundViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    queryset = MutualFunds.objects.all()
    http_method_names = ["get", "post", "patch"]

    def get_serializer_class(self):
        action = self.action
        if action == "partial_update":
            return MutualFundsUpdateSerializer
        elif action == "list":
            return MutualFundsGetSerializer
        return MutualFundsSerializer

    def get_permissions(self):
        action = self.action
        if action == "list":
            return [AllowAny()]
        elif action == "create":
            return [IsAdminUser()]
        else:
            return [IsAdminUser()]

    @extend_schema(summary="For Admin Role User")
    def create(self, request, *args, **kwargs):
        """
        Create new mutual fund object
        """
        return super().create(request, *args, **kwargs)

    @extend_schema()
    def list(self, request, *args, **kwargs):
        """
        List all mutual fund object
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="For Admin Role User")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
