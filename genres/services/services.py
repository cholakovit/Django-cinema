from genres.repo.repo import (
    create as repo_create,
    delete as repo_delete,
    get_by_id as repo_get_by_id,
    list_all as repo_list_all,
    update as repo_update,
)


def _validate_name(name: str) -> None:
    if not name or not str(name).strip():
        raise ValueError("Name is required")


def create_genre(
    name: str,
    slug: str | None = None,
    description: str | None = None,
    parent_id: str | None = None,
    color: str | None = None,
    icon: str | None = None,
):
    _validate_name(name)
    return repo_create(
        str(name).strip(),
        slug=str(slug).strip() if slug else None,
        description=description,
        parent_id=str(parent_id).strip() if parent_id else None,
        color=color,
        icon=icon,
    )


def get_genre(genre_id: str):
    return repo_get_by_id(genre_id)


def list_genres(skip: int = 0, limit: int = 100) -> list[dict[str, object]]:
    if skip < 0:
        skip = 0
    if limit <= 0 or limit > 100:
        limit = 100
    return repo_list_all(skip, limit)


def update_genre(
    genre_id: str,
    name: str | None = None,
    slug: str | None = None,
    description: str | None = None,
    parent_id: str | None = None,
    color: str | None = None,
    icon: str | None = None,
):
    existing = repo_get_by_id(genre_id)
    if not existing:
        return None
    if name is not None and not str(name).strip():
        raise ValueError("Name is required")
    return repo_update(
        genre_id,
        name=str(name).strip() if name is not None else None,
        slug=str(slug).strip() if slug is not None else None,
        description=description,
        parent_id=str(parent_id).strip() if parent_id is not None else None,
        color=color,
        icon=icon,
    )


def delete_genre(genre_id: str):
    existing = repo_get_by_id(genre_id)
    if not existing:
        return False
    repo_delete(genre_id)
    return True
