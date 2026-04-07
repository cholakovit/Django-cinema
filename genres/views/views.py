from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from pydantic import ValidationError

from genres.dto.dto import GenreCreate, GenreUpdate
from genres.services.services import (
    create_genre,
    delete_genre,
    get_genre,
    list_genres as list_genres_from_db,
    update_genre,
)
from genres.utils.responses import bad_request, not_found, parse_json_body
from utils.neo4j import node_to_json

def _genre_list_get(request: HttpRequest) -> JsonResponse:
    try:
        skip = int(request.GET.get("skip", 0))
        limit = int(request.GET.get("limit", 20))
    except ValueError:
        skip, limit = 0, 20
    rows = list_genres_from_db(skip, limit)
    return JsonResponse(
        {"items": [node_to_json(row) for row in rows]},
        safe=False,
    )

def _genre_upsert(request: HttpRequest) -> JsonResponse:
    data = parse_json_body(request)
    raw_id = data.get("id")
    if raw_id is not None and str(raw_id).strip():
        genre_id = str(raw_id).strip()
        subset = {k: data[k] for k in data if k != "id"}
        try:
            dto = GenreUpdate.model_validate(subset)
        except ValidationError as e:
            return bad_request(str(e))
        try:
            updated = update_genre(
                genre_id,
                name=dto.name,
                slug=dto.slug,
                description=dto.description,
                parent_id=dto.parent_id,
                color=dto.color,
                icon=dto.icon,
            )
        except ValueError as e:
            return bad_request(str(e))
        if not updated:
            return not_found()
        return JsonResponse(node_to_json(updated), safe=False)
    try:
        dto = GenreCreate.model_validate(data)
    except ValidationError as e:
        return bad_request(str(e))
    try:
        created = create_genre(
            dto.name,
            slug=dto.slug,
            description=dto.description,
            parent_id=dto.parent_id,
            color=dto.color,
            icon=dto.icon,
        )
    except ValueError as e:
        return bad_request(str(e))
    return JsonResponse(node_to_json(created), status=201, safe=False)

@require_http_methods(["GET", "POST"])
def genre_collection(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        return _genre_list_get(request)
    return _genre_upsert(request)

@require_http_methods(["GET", "DELETE"])
def genre_detail(request: HttpRequest, genre_id: str) -> JsonResponse:
    if request.method == "GET":
        row = get_genre(genre_id)
        if not row:
            return not_found()
        return JsonResponse(node_to_json(row), safe=False)
    ok = delete_genre(genre_id)
    if not ok:
        return not_found()
    return JsonResponse({}, status=204)

