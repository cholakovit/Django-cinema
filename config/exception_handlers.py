import neo4j.exceptions as ne
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as default_drf_exception_handler


def drf_exception_handler(exc, context):
    if isinstance(exc, ne.Neo4jError):
        return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return default_drf_exception_handler(exc, context)
