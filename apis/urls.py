from django.urls import path, include

urlpatterns = [
    path(
        "",
        include(
            [
                path("doc/", include("apis.doc.urls")), # Swagger Docs URLs
                path("", include("apis.auth.urls")), # All Auth URLs
                path("", include("apis.mutual_funds.urls")), # All Mutual Fund  URLs
                path("", include("apis.investments.urls")), # All Investment URLs + Report URL
            ]
        ),
    )
]
