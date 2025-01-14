from django.db import models

from utils.common_model import CommonModel
from utils.enums import FUND_TYPE_CHOICES
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class MutualFunds(CommonModel):
    """
    Model For Mutual Funds
    """

    name = models.CharField("Name of the mutual fund", max_length=254)
    fund_type = models.CharField(choices=FUND_TYPE_CHOICES, max_length=1)
    nav = models.FloatField("Net Asset Value", validators=[MinValueValidator(0)])

    class Meta:
        ordering = ("-created_at",)
        unique_together = (
            "name",
            "fund_type",
        )


class UserInvestments(CommonModel):
    """
    Model For User Investments
    """

    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.PROTECT,
        related_name="investments",
    )
    mutual_fund = models.ForeignKey(
        MutualFunds,
        on_delete=models.PROTECT,
        related_name="investments",
    )
    units = models.FloatField("Number of units", validators=[MinValueValidator(1)])

    class Meta:
        ordering = ("-created_at",)
        unique_together = (
            "user",
            "mutual_fund",
        )
    def clean(self):
        # Check if the units are negative
        if self.units < 1:
            raise ValidationError({'units': 'Units must be greater than or equal to 1.'})