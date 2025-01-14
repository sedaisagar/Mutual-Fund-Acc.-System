from rest_framework import serializers
from apps.accountings.models import UserInvestments


class UserInvestmentsListSerializer(serializers.ModelSerializer):
    """
    Declaring readonly serializer method field for mutual fund for getting mutual fund name in response data
    
    """
    mutual_fund = serializers.SerializerMethodField()

    def get_mutual_fund(self, instance: UserInvestments):
        return instance.mutual_fund.name

    class Meta:
        model = UserInvestments
        fields = [
            "id",
            "mutual_fund",
            "units",
        ]


class UserInvestmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInvestments
        fields = "__all__"
        extra_kwargs = {
            "user": {
                "read_only": True,
            }
        }

    def create(self, validated_data):
        """
        Create new mutual fund object if not exists otherwise add mutual fund units to existing object's units
        """
        context_user = self.context["request"].user
        investment = UserInvestments.objects.filter(
            mutual_fund=validated_data["mutual_fund"],
            user=context_user,
        ).first()

        if investment:
            return super().update(
                investment,
                {
                    #  added units to previously purchased units
                    "units": investment.units
                    + validated_data["units"],
                },
            )

        return super().create(
            {
                **validated_data,
                "user": context_user,
            }
        )


class UserReportSerializer(serializers.Serializer):
    mutual_fund = serializers.CharField(source="mutual_fund_name")
    total_units = serializers.FloatField()
    total_value = serializers.FloatField()
