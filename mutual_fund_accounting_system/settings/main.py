from .base import *

# Sqlite Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

SIMPLE_JWT = {
    "TOKEN_OBTAIN_SERIALIZER": "apis.auth.serializers.CustomTokenObtainPairSerializer",
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1 * 14),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "ISSUER": "MFAS",
    "AUTH_HEADER_TYPES": ("Bearer",),
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": ["utils.custom_renderer.CustomRenderer"],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "utils.custom_paginator.CustomPagination",
    "PAGE_SIZE": 10,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Mutual Fund Accounting System - API",
    "DESCRIPTION": "A minimal Django-based backend system to manage mutual funds and user investments, focusing on key API functionality",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SORT_OPERATIONS": False,
}
