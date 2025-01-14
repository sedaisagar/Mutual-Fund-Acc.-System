from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken


class TokenObtainAndRefreshAPITestCase(APITestCase):

    def setUp(self):
        # URL for obtaining token
        self.token_url = reverse("token_obtain")
        self.user_data = {"email": "user@example.com", "password": "string"}
        # Create a user for testing
        self.user = get_user_model().objects.create_user(**self.user_data)
        # For checking refresh token
        self.refresh_url = reverse("token_refresh")
        self.refresh_token = RefreshToken.for_user(self.user)
        self.refresh_token_str = str(self.refresh_token)

    def test_token_obtain_success(self):
        response = self.client.post(self.token_url, self.user_data, format="json")

        # Assert that the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains 'access' and 'refresh' tokens
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtain_invalid_credentials(self):
        invalid_data = {"email": "invalid@example.com", "password": "wrongpassword"}

        response = self.client.post(self.token_url, invalid_data, format="json")

        # Assert that the status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Optionally, check for an appropriate error message
        self.assertIn("errors", response.data)

    def test_token_refresh_success(self):
        response = self.client.post(
            self.refresh_url, {"refresh": self.refresh_token_str}, format="json"
        )

        # Assert that the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains a new 'access' token
        self.assertIn("access", response.data)

    def test_token_refresh_invalid_refresh_token(self):
        invalid_refresh_token = "invalid-refresh-token"

        response = self.client.post(
            self.refresh_url, {"refresh": invalid_refresh_token}, format="json"
        )

        # Assert that the status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Optionally, check for an appropriate error message
        self.assertIn("errors", response.data)
