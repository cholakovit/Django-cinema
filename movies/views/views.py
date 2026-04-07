from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from pydantic import ValidationError

from movies.dto.movie import MovieCreate, MovieResponse, MovieUpdate
from movies.services.services import (
    create_movie,
    delete_movie,
    get_movie,
    list_movies as list_movies_from_db,
    update_movie,
)
from movies.utils.responses import bad_request, not_found, parse_json_body
from utils.neo4j import node_to_json


def _movie_to_payload(row: dict[str, object]) -> dict[str, object]:
    return MovieResponse.model_validate(node_to_json(row)).model_dump(mode="json")


def _movie_list_get(request: HttpRequest) -> JsonResponse:
    try:
        skip = int(request.GET.get("skip", 0))
        limit = int(request.GET.get("limit", 20))
    except ValueError:
        skip, limit = 0, 20
    rows = list_movies_from_db(skip, limit)
    return JsonResponse(
        {"items": [_movie_to_payload(row) for row in rows]},
        safe=False,
    )


def _movie_upsert(request: HttpRequest) -> JsonResponse:
    data = parse_json_body(request)
    raw_id = data.get("id")
    if raw_id is not None and str(raw_id).strip():
        movie_id = str(raw_id).strip()
        subset = {k: data[k] for k in data if k != "id"}
        try:
            dto = MovieUpdate.model_validate(subset)
        except ValidationError as e:
            return bad_request(str(e))
        try:
            updated = update_movie(
                movie_id,
                name=dto.name,
                year=dto.year,
                description=dto.description,
                rating=dto.rating,
            )
        except ValueError as e:
            return bad_request(str(e))
        if not updated:
            return not_found()
        return JsonResponse(_movie_to_payload(updated), safe=False)
    try:
        dto = MovieCreate.model_validate(data)
    except ValidationError as e:
        return bad_request(str(e))
    try:
        created = create_movie(
            dto.name,
            year=dto.year,
            description=dto.description,
            rating=dto.rating,
        )
    except ValueError as e:
        return bad_request(str(e))
    return JsonResponse(_movie_to_payload(created), status=201, safe=False)


@require_http_methods(["GET", "POST"])
def movie_collection(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        return _movie_list_get(request)
    return _movie_upsert(request)


@require_http_methods(["GET", "DELETE"])
def movie_detail(request: HttpRequest, movie_id: str) -> JsonResponse:
    if request.method == "GET":
        row = get_movie(movie_id)
        if not row:
            return not_found()
        return JsonResponse(_movie_to_payload(row), safe=False)
    ok = delete_movie(movie_id)
    if not ok:
        return not_found()
    return JsonResponse({}, status=204)
