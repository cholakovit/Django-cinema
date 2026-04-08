from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.dto.dto import MovieCreate, MovieUpdate
from movies.services.services import (
    create_movie,
    delete_movie,
    get_movie,
    list_movies as list_movies_from_db,
    update_movie,
)
from utils.helper import movie_row_to_payload


class MovieCollectionView(APIView):
    def get(self, request):
        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 20))
        except ValueError:
            skip, limit = 0, 20
        rows = list_movies_from_db(skip, limit)
        return Response(
            {"items": [movie_row_to_payload(row) for row in rows]},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        data = request.data if isinstance(request.data, dict) else {}
        raw_id = data.get("id")
        if raw_id is not None and str(raw_id).strip():
            movie_id = str(raw_id).strip()
            subset = {k: data[k] for k in data if k != "id"}
            try:
                dto = MovieUpdate.model_validate(subset)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            try:
                updated = update_movie(
                    movie_id,
                    name=dto.name,
                    year=dto.year,
                    description=dto.description,
                    rating=dto.rating,
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            if not updated:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(movie_row_to_payload(updated), status=status.HTTP_200_OK)
        try:
            dto = MovieCreate.model_validate(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            created = create_movie(
                dto.name,
                year=dto.year,
                description=dto.description,
                rating=dto.rating,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(movie_row_to_payload(created), status=status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    def get(self, request, movie_id):
        row = get_movie(movie_id)
        if not row:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(movie_row_to_payload(row), status=status.HTTP_200_OK)

    def delete(self, request, movie_id):
        ok = delete_movie(movie_id)
        if not ok:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
