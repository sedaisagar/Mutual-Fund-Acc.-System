from rest_framework.response import Response
from rest_framework.compat import (
    INDENT_SEPARATORS,
    LONG_SEPARATORS,
    SHORT_SEPARATORS,
)
import json
from rest_framework.renderers import JSONRenderer
import importlib


class CustomRenderer(JSONRenderer):
    def get_error_type(self, data):
        if "type" in data:
            match data["type"].__str__():
                case "ErrorType.CLIENT_ERROR":
                    return "Client Error"
                case "ErrorType.SERVER_ERROR":
                    return "Server Error"
                case "ErrorType.VALIDATION_ERROR":
                    return "Validation Error"
            return "Unknown Error"
        return "Operation Success"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {
            "message": self.get_error_type(data),
            "data": data,
        }
        return super().render(data, accepted_media_type, renderer_context)