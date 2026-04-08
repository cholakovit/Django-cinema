from movies.repositories.repo import (
    create as repo_create,
    delete as repo_delete,
    get_by_id as repo_get_by_id,
    list_all as repo_list_all,
    update as repo_update,
)


def create_movie(name, year=None, description=None, rating=None):
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
    return repo_update(
        movie_id,
        name=name,
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
