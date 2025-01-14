from django.urls import path, include

urlpatterns = [
    path(
        "",
        include(
            [
                path("doc/", include("apis.doc.urls")),
                path("", include("apis.auth.urls")),
                path("", include("apis.mutual_funds.urls")),
                path("", include("apis.investments.urls")),
            ]
        ),
    )
]
