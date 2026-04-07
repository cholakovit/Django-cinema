from django.urls import include, path

urlpatterns = [
    path(
        "api/v1/",
        include(
            [
                path("", include("movies.urls")),
                path("", include("genres.urls")),
            ]
        ),
    ),
]
