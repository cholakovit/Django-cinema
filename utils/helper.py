from movies.dto.dto import MovieResponse
from utils.neo4j import node_to_json


def movie_row_to_payload(row: dict[str, object]) -> dict[str, object]:
    return MovieResponse.model_validate(node_to_json(row)).model_dump(mode="json")
