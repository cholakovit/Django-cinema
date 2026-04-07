from movies.repositories.repo import (
    create as repo_create,
    delete as repo_delete,
    get_by_id as repo_get_by_id,
    list_all as repo_list_all,
    update as repo_update,
)


def create_movie(name, year=None, description=None, rating=None):
    if not name or not str(name).strip():
        raise ValueError("Name is required")
    if year is not None and (not isinstance(year, int) or year < 0):
        raise ValueError("Year must be a positive integer")
    if rating is not None and (
        not isinstance(rating, (int, float)) or rating < 0 or rating > 10
    ):
        raise ValueError("Rating must be a number between 0 and 10")
    return repo_create(name, year, description, rating)


def get_movie(movie_id):
    return repo_get_by_id(movie_id)


def list_movies(skip=0, limit=20):
    if skip < 0:
        skip = 0
    if limit <= 0 or limit > 100:
        limit = 20
    return repo_list_all(skip, limit)


def update_movie(movie_id, name=None, year=None, description=None, rating=None):
    existing = repo_get_by_id(movie_id)
    if not existing:
        return None
    if name is not None and not str(name).strip():
        raise ValueError("Name is required")
    if year is not None and (not isinstance(year, int) or year < 0):
        raise ValueError("Year must be a positive integer")
    if rating is not None and (
        not isinstance(rating, (int, float)) or rating < 0 or rating > 10
    ):
        raise ValueError("Rating must be a number between 0 and 10")
    return repo_update(
        movie_id,
        name=str(name).strip() if name is not None else None,
        year=year,
        description=description,
        rating=rating,
    )


def delete_movie(movie_id):
    existing = repo_get_by_id(movie_id)
    if not existing:
        return False
    repo_delete(movie_id)
    return True
