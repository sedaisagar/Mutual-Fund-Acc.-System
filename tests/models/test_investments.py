from django.test import TestCase
from django.db.utils import IntegrityError
from apps.authentication.models import User
from apps.accountings.models import MutualFunds, UserInvestments


class UserInvestmentsModelTest(TestCase):

    def setUp(self):
        # Sample data for user and mutual funds
        self.user_data = {
            "email": "user@example.com",
        }

        self.mutual_fund_data_1 = {
            "name": "Blue Chip Fund",
            "fund_type": "E",  # Assuming 'E' for Equity
            "nav": 150.5,
        }

        self.mutual_fund_data_2 = {
            "name": "Debt Secure Fund",
            "fund_type": "D",  # Assuming 'D' for Debt
            "nav": 100.0,
        }

        # Create test user and mutual funds
        self.user = User.objects.create(**self.user_data)
        self.mutual_fund_1 = MutualFunds.objects.create(**self.mutual_fund_data_1)
        self.mutual_fund_2 = MutualFunds.objects.create(**self.mutual_fund_data_2)

        # Create investment data
        self.investment_data_1 = {
            "user": self.user,
            "mutual_fund": self.mutual_fund_1,
            "units": 50.0,
        }
        self.investment_data_2 = {
            "user": self.user,
            "mutual_fund": self.mutual_fund_2,
            "units": 30.0,
        }

    def test_create_user_investment(self):
        # Create user investment
        investment_1 = UserInvestments.objects.create(**self.investment_data_1)

        # Check if the investment is correctly created
        self.assertEqual(investment_1.user, self.user)
        self.assertEqual(investment_1.mutual_fund, self.mutual_fund_1)
        self.assertEqual(investment_1.units, 50.0)

    def test_investment_unique_together(self):
        # Create the first investment
        UserInvestments.objects.create(**self.investment_data_1)

        # Try creating another investment with the same user and mutual fund (should raise IntegrityError)
        with self.assertRaises(IntegrityError):
            UserInvestments.objects.create(
                **self.investment_data_1
            )  # Same user and same mutual fund

    def test_investment_multiple_funds_for_user(self):
        # Create investments for the same user but different mutual funds
        investment_1 = UserInvestments.objects.create(**self.investment_data_1)
        investment_2 = UserInvestments.objects.create(**self.investment_data_2)

        # Check if both investments are created correctly
        self.assertEqual(investment_1.user, self.user)
        self.assertEqual(investment_2.user, self.user)
        self.assertEqual(investment_1.mutual_fund, self.mutual_fund_1)
        self.assertEqual(investment_2.mutual_fund, self.mutual_fund_2)

    def test_investment_units_field(self):
        # Create an investment with valid units
        investment_1 = UserInvestments.objects.create(
            user=self.user,
            mutual_fund=self.mutual_fund_1,
            units=100.0,
        )

        # Check if units are stored correctly
        self.assertEqual(investment_1.units, 100.0)

    def test_investment_ordering(self):
        # Create two investments for the user
        investment_1 = UserInvestments.objects.create(**self.investment_data_1)
        investment_2 = UserInvestments.objects.create(**self.investment_data_2)

        # Ensure that the investments are ordered by created_at in descending order
        investments = UserInvestments.objects.all()
        self.assertEqual(
            investments[0], investment_1
        )  # The most recent investment should come first
        self.assertEqual(investments[1], investment_2)

    def test_protect_on_delete(self):
        # Test that trying to delete a user or mutual fund with investments will raise a ProtectedError
        investment_1 = UserInvestments.objects.create(**self.investment_data_1)

        # Try deleting the user, which should raise a ProtectedError because of the ForeignKey with PROTECT
        with self.assertRaises(IntegrityError):
            self.user.delete()  # Should raise ProtectedError

        # Try deleting the mutual fund, which should also raise a ProtectedError
        with self.assertRaises(IntegrityError):
            self.mutual_fund_1.delete()  # Should raise ProtectedError
