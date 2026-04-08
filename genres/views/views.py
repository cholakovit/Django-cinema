from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from genres.dto.dto import GenreCreate, GenreUpdate
from genres.services.services import (
    create_genre,
    delete_genre,
    get_genre,
    list_genres as list_genres_from_db,
    update_genre,
)
from utils.neo4j import node_to_json


class GenreCollectionView(APIView):
    def get(self, request):
        try:
            skip = int(request.query_params.get("skip", 0))
            limit = int(request.query_params.get("limit", 20))
        except ValueError:
            skip, limit = 0, 20
        rows = list_genres_from_db(skip, limit)
        return Response(
            {"items": [node_to_json(row) for row in rows]},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        data = request.data if isinstance(request.data, dict) else {}
        raw_id = data.get("id")
        if raw_id is not None and str(raw_id).strip():
            genre_id = str(raw_id).strip()
            subset = {k: data[k] for k in data if k != "id"}
            try:
                dto = GenreUpdate.model_validate(subset)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            try:
                updated = update_genre(genre_id, dto)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            if not updated:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(node_to_json(updated), status=status.HTTP_200_OK)
        try:
            dto = GenreCreate.model_validate(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            created = create_genre(dto)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(node_to_json(created), status=status.HTTP_201_CREATED)


class GenreDetailView(APIView):
    def get(self, request, genre_id):
        row = get_genre(genre_id)
        if not row:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(node_to_json(row), status=status.HTTP_200_OK)

    def delete(self, request, genre_id):
        ok = delete_genre(genre_id)
        if not ok:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
