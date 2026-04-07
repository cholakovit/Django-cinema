import json

from django.http import HttpRequest, JsonResponse


def parse_json_body(request: HttpRequest) -> dict[str, object]:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def bad_request(message: str) -> JsonResponse:
    return JsonResponse({"error": message}, status=400)


def not_found() -> JsonResponse:
    return JsonResponse({"error": "Not found"}, status=404)
