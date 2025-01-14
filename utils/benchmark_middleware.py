# core/middleware.py

import time
from django.db import connection, reset_queries
from django.http import HttpResponse, HttpRequest


def benchmark(get_response):
    """
    Middleware that prints total time consumed for number of queries between single request - response
    """

    def middleware(request: HttpRequest):

        reset_queries()
        # Get beginning stats
        start_queries = len(connection.queries)
        start_time = time.perf_counter()

        # Process the request
        response = get_response(request)

        # Get ending stats
        end_time = time.perf_counter()
        end_queries = len(connection.queries)

        # Calculate stats
        total_time = end_time - start_time
        total_queries = end_queries - start_queries

        print(
            ">>>> Start queries",
            start_queries,
            "End queries",
            end_queries,
            "Total queries",
            total_queries,
            "Total time",
            total_time,
            "<<<<<<<<<<",
        )
        
        return response

    return middleware
