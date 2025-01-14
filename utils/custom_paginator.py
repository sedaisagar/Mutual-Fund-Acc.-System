from rest_framework import pagination
from rest_framework.renderers import JSONRenderer

from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data):
        
        response_data = {
            "results": data,
            "pagination": {
                "current_limit": self.page.paginator.per_page,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "current_page": self.page.number,
            },
        }

        return Response(response_data)
