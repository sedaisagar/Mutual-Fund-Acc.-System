from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserRegisterAPITestCase(APITestCase):
    def setUp(self):
        # URL for user registration
        self.register_url = reverse("user_register")  
        self.valid_payload = {
            "email": "user@example.com",
            "password": "string",
        }
        self.invalid_payload = {
            "email": "user@examples.com",
            # Missing password
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        
        # Assert that the status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Optionally, you can check if the response contains the correct data
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], self.valid_payload['email'])
    
    def test_user_registration_missing_fields(self):
        response = self.client.post(self.register_url, self.invalid_payload, format='json')
        
        # Assert that the status code is 400 (Bad Request) because of missing password
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check for validation  errors on missing field
        self.assertIn("errors",response.data)
