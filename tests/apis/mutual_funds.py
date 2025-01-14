from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.accountings.models import MutualFunds
from django.contrib.auth import get_user_model


class MutualFundViewSetTestCase(APITestCase):
    
    def setUp(self):
        # Create an admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="password123"
        )
        
        # Create a regular user
        self.regular_user = get_user_model().objects.create_user(
            email="user@example.com", password="password123"
        )
        
        # Create a mutual fund instance for testing
        self.mutual_fund = MutualFunds.objects.create(
            name="Test Mutual Fund", fund_type="E", nav=10.0
        )
        
        # API URL
        self.mutual_fund_url = reverse("mutual_funds-list")  # List URL
        self.mutual_fund_detail_url = reverse("mutual_funds-detail", kwargs={"pk": self.mutual_fund.id})  # Detail URL for update

    def test_list_mutual_funds_success(self):
        """
        Ensure that the list of mutual funds is accessible by any user (AllowAny permission).
        """
        response = self.client.get(self.mutual_fund_url)
        
        # Assert that the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        


    def test_create_mutual_fund_admin(self):
        """
        Ensure that only admins can create a new mutual fund.
        """
        self.client.force_authenticate(user=self.admin_user)  # Authenticate as admin
        
        payload = {
            "name": "Blue Chip Fund",
            "fund_type": "E",  # Assume E is for Equity
            "nav": 0
        }
        
        response = self.client.post(self.mutual_fund_url, payload, format="json")
        
        # Assert that the status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
     

    def test_create_mutual_fund_regular_user(self):
        """
        Ensure that regular users cannot create a new mutual fund.
        """
        self.client.force_authenticate(user=self.regular_user)  # Authenticate as regular user
        
        payload = {
            "name": "New Mutual Fund",
            "fund_type": "D",  # Assume D is for Debt
            "nav": 150.5
        }
        
        response = self.client.post(self.mutual_fund_url, payload, format="json")
        
        # Assert that the status code is 403 (Forbidden) for regular users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_mutual_fund_admin(self):
        """
        Ensure that only admins can partially update a mutual fund.
        """
         # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user) 
        
        payload = {
            "nav": 10
        }
        
        response = self.client.patch(self.mutual_fund_detail_url, payload, format="json")
        
        # Assert that the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
        # Check that the nav value is updated
        # Refresh the instance from the database
        self.mutual_fund.refresh_from_db()  
        self.assertEqual(self.mutual_fund.nav, payload["nav"])

    def test_partial_update_mutual_fund_regular_user(self):
        """
        Ensure that regular users cannot partially update a mutual fund.
        """
        self.client.force_authenticate(user=self.regular_user)  # Authenticate as regular user
        
        payload = {
            "nav": 200.0
        }
        
        response = self.client.patch(self.mutual_fund_detail_url, payload, format="json")
        
        # Assert that the status code is 403 (Forbidden) for regular users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
