from django.urls import path
from django.views.generic import RedirectView

from genres.views.pages import GenreCreatePageView, GenreDetailPageView, GenreListPageView, GenreDeletePageView
from genres.views.views import GenreCollectionView, GenreDetailView

urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="genre_list_page", permanent=False),
    ),
    path("genres/create/", GenreCreatePageView.as_view(), name="genre_create_page"),
    path(
        "genres/<str:genre_id>/",
        GenreDetailPageView.as_view(),
        name="genre_detail_page",
    ),
    path("genres/", GenreListPageView.as_view(), name="genre_list_page"),
    path("api/v1/genres/", GenreCollectionView.as_view(), name="genre_collection"),
    path(
        "api/v1/genres/<str:genre_id>/",
        GenreDetailView.as_view(),
        name="genre_detail",
    ),
    path(
        "genres/<str:genre_id>/delete/",
        GenreDeletePageView.as_view(),
        name="genre_delete_page",
    )
]
