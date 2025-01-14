from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    doc = """
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mutual Fund Accounting System</title>
        </head>
        <body>
            <h1>Welcome !!!</h1>

            <!-- Link to the Swagger Docs -->
            <p><a href="/api/doc/">Swagger Documentation</a></p>
        </body>
        </html>
    """
    return HttpResponse(doc)
