import uuid
from datetime import datetime, timezone

from db.neo4j import get_driver


def _normalize_movie(props: dict[str, object], *, element_id: str | None = None) -> dict[str, object]:
    raw_id = props.get("id")
    if raw_id is not None and str(raw_id).strip():
        out_id = str(raw_id).strip()
    elif props.get("tmdb_id") is not None:
        out_id = str(props["tmdb_id"]).strip()
    elif element_id:
        out_id = element_id
    else:
        out_id = ""

    name = props.get("name") or props.get("title")
    if not name or not str(name).strip():
        name = "Unknown"
    else:
        name = str(name).strip()

    desc = props.get("description")
    if desc is None or (isinstance(desc, str) and not desc.strip()):
        desc = props.get("overview")
    if isinstance(desc, str):
        desc = desc.strip() or None

    year = props.get("year")
    if year is not None:
        try:
            year = int(year)
        except (TypeError, ValueError):
            year = None

    rating = props.get("rating")
    if rating is None:
        rating = props.get("vote_average")
    if rating is not None:
        try:
            rating = float(rating)
        except (TypeError, ValueError):
            rating = None

    created = props.get("created_at")
    if created is None:
        created = datetime(1970, 1, 1, tzinfo=timezone.utc)

    return {
        "id": out_id,
        "name": name,
        "type": "movie",
        "year": year,
        "description": desc,
        "rating": rating,
        "created_at": created,
    }


def create(name, year=None, description=None, rating=None):
    driver = get_driver()
    uid = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    with driver.session() as session:
        session.run(
            f"""
            CREATE (m:Movie {{
                id: $id, name: $name, type: 'movie',
                year: $year, description: $description, rating: $rating,
                created_at: $created_at
            }}) RETURN m
            """,
            id=uid,
            name=name,
            year=year,
            description=description or "",
            rating=float(rating) if rating is not None else None,
            created_at=now,
        )
    return get_by_id(uid)


def get_by_id(movie_id):
    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            """
            MATCH (m:Movie)
            WHERE m.id = $id
               OR (m.tmdb_id IS NOT NULL AND toString(m.tmdb_id) = $id)
               OR elementId(m) = $id
            WITH m, elementId(m) AS eid
            RETURN properties(m) AS p, eid
            LIMIT 1
            """,
            id=movie_id,
        )
        record = result.single()
        if not record:
            return None
        return _normalize_movie(dict(record["p"]), element_id=record["eid"])


def list_all(skip=0, limit=20):
    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            """
            MATCH (m:Movie)
            WITH m, elementId(m) AS eid,
                 coalesce(m.created_at, datetime('1970-01-01T00:00:00Z')) AS sort_ts
            ORDER BY sort_ts DESC
            SKIP $skip
            LIMIT $limit
            RETURN properties(m) AS p, eid
            """,
            skip=skip,
            limit=limit,
        )
        return [_normalize_movie(dict(record["p"]), element_id=record["eid"]) for record in result]


def update(movie_id, name=None, year=None, description=None, rating=None):
    driver = get_driver()
    updates = []
    params = {"id": movie_id}
    if name is not None:
        updates.append("m.name = $name")
        params["name"] = name
    if year is not None:
        updates.append("m.year = $year")
        params["year"] = year
    if description is not None:
        updates.append("m.description = $description")
        params["description"] = description
    if rating is not None:
        updates.append("m.rating = $rating")
        params["rating"] = float(rating) if rating is not None else None
    if not updates:
        return get_by_id(movie_id)
    set_clause = ", ".join(updates)
    with driver.session() as session:
        session.run(f"MATCH (m:Movie {{id: $id}}) SET {set_clause} RETURN m", **params)
    return get_by_id(movie_id)


def delete(movie_id):
    driver = get_driver()
    with driver.session() as session:
        session.run("MATCH (m:Movie {id: $id}) DETACH DELETE m", id=movie_id)
