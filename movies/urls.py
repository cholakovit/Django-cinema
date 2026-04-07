from django.urls import path

from movies import views

urlpatterns = [
    path("movies/", views.movie_collection, name="movie_collection"),
    path("movies/<str:movie_id>/", views.movie_detail, name="movie_detail"),
]
