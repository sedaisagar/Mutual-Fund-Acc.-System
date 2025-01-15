from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.accountings.models import MutualFunds, UserInvestments


class UserInvestmentsViewSetTestCase(APITestCase):
    
    def setUp(self):
        # Create users
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="password123"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="password123"
        )
        
        # Create a mutual fund for the investment
        self.mutual_fund = MutualFunds.objects.create(
            name="Blue Chip Fund", fund_type="E", nav=100.0
        )
        
        # URL for investments and reports
        self.investments_url = reverse("user_investments-list")
        self.report_url = reverse("user_investment_reports-list")
        
        # Creating a UserInvestment instance for testing
        self.user_investment = UserInvestments.objects.create(
            user=self.user,
            mutual_fund=self.mutual_fund,
            units=10,
        )

    def test_create_investment_as_authenticated_user(self):
        """Test creating an investment for authenticated user"""
        self.client.force_authenticate(user=self.user)
        
        payload = {
            "mutual_fund": self.mutual_fund.id,
            "units": 10,
        }
        # This post should not have created new investment, rather added units to investment object
        response = self.client.post(self.investments_url, payload, format="json")
        
        # Assert that the status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertNotEqual(response.data["units"], 10)
        self.assertEqual(response.data["units"], 20)

        

    def test_create_investment_as_unauthenticated_user(self):
        """Test creating an investment for unauthenticated user"""
        payload = {
            "user": self.user.id,
            "mutual_fund": self.mutual_fund.id,
            "units": 10,
        }
        
        response = self.client.post(self.investments_url, payload, format="json")
        
        # Assert that the status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_investments_as_authenticated_user(self):
        """Test listing investments for authenticated user"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.investments_url)
        
        # Assert that the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_investments_as_unauthenticated_user(self):
        """Test listing investments for unauthenticated user"""
        response = self.client.get(self.investments_url)
        
        # Assert that the status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReportGenerateViewTestCase(APITestCase):

    def setUp(self):
        # Create users
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="password123"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="password123"
        )
        
        # Create mutual fund for investment
        self.mutual_fund = MutualFunds.objects.create(
            name="Blue Chip Fund", fund_type="E", nav=100.0
        )
        
        # Create UserInvestments for the report
        self.user_investment = UserInvestments.objects.create(
            user=self.user,
            mutual_fund=self.mutual_fund,
            units=10,
        )
        
        # URL for report
        self.report_url = reverse("user_investment_reports-list")
        
    def test_generate_report_as_authenticated_user(self):
        """Test generating investment report for authenticated user"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.report_url)
        
        # Assert that the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_generate_report_as_unauthenticated_user(self):
        """Test generating investment report for unauthenticated user"""
        response = self.client.get(self.report_url)
        
        # Assert that the status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
