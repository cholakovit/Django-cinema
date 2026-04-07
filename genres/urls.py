from django.urls import path
from genres import views

urlpatterns = [
    path("genres/", views.genre_collection, name="genre_collection"),
    path("genres/<str:genre_id>/", views.genre_detail, name="genre_detail"),
]