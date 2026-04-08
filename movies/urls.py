from django.urls import path

from movies.views.views import MovieCollectionView, MovieDetailView

urlpatterns = [
    path("movies/", MovieCollectionView.as_view(), name="movie_collection"),
    path("movies/<str:movie_id>/", MovieDetailView.as_view(), name="movie_detail"),
]
