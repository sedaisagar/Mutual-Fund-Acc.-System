from rest_framework import generics, status
from rest_framework.response import Response
from apps.authentication.models import User
from .serializers import UserRegistrationSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from utils.custom_paginator import CustomPagination


@extend_schema_view(
    post=extend_schema(
        summary="User registration api",
        tags=["Auth"],
    )
)
class UserRegistrationView(generics.CreateAPIView):
    """
    Create new user with email and password
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs): 
        # Use the DRF's built-in functionality to handle the data validation and saving
        serializer = self.get_serializer(data=request.data.copy())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Prepare headers and respond with the newly created user data
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
