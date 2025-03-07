from django.contrib.auth.models import BaseUserManager


# Custom Manager to handle user creation
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """

        if not email:
            raise ValueError("The Email field can't be empty !")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("role", "A")
        return self.create_user(email, password, **extra_fields)
