from django.urls import path

from genres.views.views import GenreCollectionView, GenreDetailView

urlpatterns = [
    path("genres/", GenreCollectionView.as_view(), name="genre_collection"),
    path("genres/<str:genre_id>/", GenreDetailView.as_view(), name="genre_detail"),
]
