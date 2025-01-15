from django.test import TestCase

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

class UserModelTestCase(TestCase):
    def setUp(self):
        # Create a user instance with a specific email and role
        self.user_data = {
            "email": "testuser@example.com",
            "role": "U",  # User role
        }
        self.admin_data = {
            "email": "adminuser@example.com",
            "role": "A" , # Admin role
        }

    def test_create_user(self):
        # Create a regular user
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.role, self.user_data["role"])
        self.assertFalse(user.is_staff)  # Default role "U" should not be staff
        self.assertFalse(user.is_superuser)  # Default role "U" should not be superuser

    def test_create_superuser(self):
        # Create a superuser
        admin = get_user_model().objects.create_user(**self.admin_data)
        self.assertEqual(admin.email, self.admin_data["email"])
        self.assertEqual(admin.role, self.admin_data["role"])
        self.assertTrue(admin.is_staff)  # Admin role should have is_staff as True
        self.assertTrue(admin.is_superuser)  # Admin role should have is_superuser as True

    def test_email_uniqueness(self):
        # Ensure that the email field is unique
        get_user_model().objects.create_user(**self.user_data)
        
        with self.assertRaises(IntegrityError):
            # Try creating another user with the same email
            get_user_model().objects.create_user(email=self.user_data["email"], role="U")

    def test_str_method(self):
        # Test the __str__ method of the User model
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data["email"])

    def test_is_staff_property(self):
        # Test that the is_staff property works correctly based on the role
        user = get_user_model().objects.create_user(**self.user_data)
        admin = get_user_model().objects.create_user(**self.admin_data)
        
        self.assertFalse(user.is_staff)  # Regular user should not be staff
        self.assertTrue(admin.is_staff)  # Admin user should be staff

    def test_is_superuser_property(self):
        # Test that the is_superuser property works correctly based on the role
        user = get_user_model().objects.create_user(**self.user_data)
        admin = get_user_model().objects.create_user(**self.admin_data)
        
        self.assertFalse(user.is_superuser)  # Regular user should not be superuser
        self.assertTrue(admin.is_superuser)  # Admin user should be superuser
