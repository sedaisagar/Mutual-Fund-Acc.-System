from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.authentication.models import User
from django.contrib.auth.hashers import make_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
        ]
        extra_kwargs = {
            "password":{
                "write_only":True,
            }
        }

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        data = super().validate(
            attrs,
        )
        nData = {"id": self.user.id, "role": self.user.role, "email": self.user.email}

        return {**nData, **data}


from drf_spectacular.utils import extend_schema, extend_schema_view

from drf_spectacular.extensions import OpenApiViewExtension


class FixTokenObtainPairView(OpenApiViewExtension):
    target_class = "rest_framework_simplejwt.views.TokenObtainPairView"

    def view_replacement(self):
        return extend_schema_view(
            post=extend_schema(
                summary="Token Obtain pair api ",
                tags=["Auth"],
            )
        )(self.target_class)


class FixTokenRefreshPairView(OpenApiViewExtension):
    target_class = "rest_framework_simplejwt.views.TokenRefreshView"

    def view_replacement(self):
        return extend_schema_view(
            post=extend_schema(
                summary="Token Refresh api ",
                tags=["Auth"],
            )
        )(self.target_class)
