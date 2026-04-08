from genres.dto.dto import GenreCreate, GenreUpdate
from genres.repo.repo import (
    create as repo_create,
    delete as repo_delete,
    get_by_id as repo_get_by_id,
    list_all as repo_list_all,
    update as repo_update,
)


def create_genre(data: GenreCreate):
    return repo_create(data)


def get_genre(genre_id: str):
    return repo_get_by_id(genre_id)


def list_genres(skip: int = 0, limit: int = 100) -> list[dict[str, object]]:
    if skip < 0:
        skip = 0
    if limit <= 0 or limit > 100:
        limit = 100
    return repo_list_all(skip, limit)


def update_genre(genre_id: str, patch: GenreUpdate):
    existing = repo_get_by_id(genre_id)
    if not existing:
        return None
    return repo_update(genre_id, patch)


def delete_genre(genre_id: str):
    existing = repo_get_by_id(genre_id)
    if not existing:
        return False
    repo_delete(genre_id)
    return True
