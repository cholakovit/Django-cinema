import uuid
from datetime import datetime
from db.neo4j import get_driver


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
            "MATCH (m:Movie {id: $id}) RETURN m",
            id=movie_id,
        )
        record = result.single()
        if not record:
            return None
        node = record["m"]
        return dict(node)


def list_all(skip=0, limit=20):
    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            "MATCH (m:Movie) RETURN m ORDER BY m.created_at DESC SKIP $skip LIMIT $limit",
            skip=skip,
            limit=limit,
        )
        return [dict(record["m"]) for record in result]


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
