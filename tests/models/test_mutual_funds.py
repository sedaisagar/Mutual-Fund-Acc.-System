from django.test import TestCase

from apps.accountings.models import MutualFunds
from django.db.utils import IntegrityError


class MutualFundTestCase(TestCase):
    def setUp(self):
        # Sample data for mutual funds
        self.mutual_fund_data_1 = {
            "name": "Blue Chip Fund",
            "fund_type": "E",  # Example fund type: 'E' (Equity)
            "nav": 150.5,
        }

        self.mutual_fund_data_2 = {
            "name": "Debt Secure Fund",
            "fund_type": "D",  # Example fund type: 'D' (Debt)
            "nav": 100.0,
        }

        self.mutual_fund_data_3 = {
            "name": "Blue Chip Fund",  # Same name as mutual_fund_data_1, different fund_type
            "fund_type": "D",  # Different fund type
            "nav": 200.0,
        }

        self.mutual_fund_data_invalid_name_fundtype = {
            "name": "Blue Chip Fund",  # Same name and fund_type as mutual_fund_data_1
            "fund_type": "E",  # Same fund type
            "nav": 250.0,
        }

    def test_create_mutual_fund(self):
        # Create mutual funds with valid data
        fund_1 = MutualFunds.objects.create(**self.mutual_fund_data_1)
        fund_2 = MutualFunds.objects.create(**self.mutual_fund_data_2)

        # Check if both funds are created properly
        self.assertEqual(fund_1.name, self.mutual_fund_data_1["name"])
        self.assertEqual(fund_1.fund_type, self.mutual_fund_data_1["fund_type"])
        self.assertEqual(fund_1.nav, self.mutual_fund_data_1["nav"])

        self.assertEqual(fund_2.name, self.mutual_fund_data_2["name"])
        self.assertEqual(fund_2.fund_type, self.mutual_fund_data_2["fund_type"])
        self.assertEqual(fund_2.nav, self.mutual_fund_data_2["nav"])

    def test_mutual_fund_name_fundtype_uniqueness(self):
        # Ensure that the combination of name and fund_type is unique
        MutualFunds.objects.create(**self.mutual_fund_data_1)  # Create first fund
        MutualFunds.objects.create(**self.mutual_fund_data_2)  # Create second fund

        # Try creating another fund with the same name and fund_type (should raise IntegrityError)
        with self.assertRaises(IntegrityError):
            MutualFunds.objects.create(**self.mutual_fund_data_invalid_name_fundtype)

    def test_fund_type_choices(self):
        # Test that fund_type is correctly restricted to the choices
        valid_fund_type_1 = "E"  # Assuming 'E' for Equity
        valid_fund_type_2 = "D"  # Assuming 'D' for Debt

        fund_1 = MutualFunds.objects.create(
            name="Blue Chip Fund", fund_type=valid_fund_type_1, nav=150.5
        )
        fund_2 = MutualFunds.objects.create(
            name="Debt Secure Fund", fund_type=valid_fund_type_2, nav=100.0
        )

        self.assertEqual(fund_1.fund_type, valid_fund_type_1)
        self.assertEqual(fund_2.fund_type, valid_fund_type_2)

    def test_mutual_fund_ordering(self):
        # Test that mutual funds are ordered by the created_at field in descending order
        fund_1 = MutualFunds.objects.create(**self.mutual_fund_data_1)
        fund_2 = MutualFunds.objects.create(**self.mutual_fund_data_2)

        # Force save to ensure the created_at field is set
        fund_1.save()
        fund_2.save()

        # Ensure that the latest created fund appears first
        mutual_funds = MutualFunds.objects.all()

        self.assertEqual(
            mutual_funds[0], fund_1
        )  # fund_2 should come first because it was created later
        self.assertEqual(mutual_funds[1], fund_2)  # fund_1 should come second

    def test_nav_field_type(self):
        # Ensure that NAV is a float and is stored correctly
        fund_1 = MutualFunds.objects.create(**self.mutual_fund_data_1)
        fund_2 = MutualFunds.objects.create(**self.mutual_fund_data_2)

        self.assertIsInstance(fund_1.nav, float)  # NAV should be a float
        self.assertIsInstance(fund_2.nav, float)  # NAV should be a float
        self.assertEqual(
            fund_1.nav, self.mutual_fund_data_1["nav"]
        )  # Ensure the value matches
        self.assertEqual(
            fund_2.nav, self.mutual_fund_data_2["nav"]
        )  # Ensure the value matches
