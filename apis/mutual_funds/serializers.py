from rest_framework import serializers
from apps.accountings.models import MutualFunds


class MutualFundsGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = MutualFunds
        fields = [
            "id",
            "name",
            "fund_type",
            "nav",
        ]


class MutualFundsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutualFunds
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class MutualFundsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutualFunds
        fields = ["nav"]
        extra_kwargs = {}
