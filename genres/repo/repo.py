import uuid
from datetime import datetime, timezone

from db.neo4j import get_driver
from genres.dto.dto import GenreCreate, GenreUpdate

_PATCH_KEYS = frozenset(
    ("name", "slug", "description", "parent_id", "color", "icon"),
)

_MATCH_GENRE = """
MATCH (g:Genre)
WHERE (g.id IS NOT NULL AND g.id = $id) OR elementId(g) = $id
"""


def _row_with_id(p: dict[str, object], eid: object) -> dict[str, object]:
    raw = p.get("id")
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        p = {**p, "id": eid}
    return p


def create(data: GenreCreate) -> dict[str, object] | None:
    d = data.model_dump()
    driver = get_driver()
    uid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with driver.session() as session:
        session.run(
            """
            CREATE (g:Genre {
              id: $id, name: $name, slug: $slug, type: 'genre',
              description: $description, parent_id: $parent_id,
              color: $color, icon: $icon, created_at: $created_at}) RETURN g
            """,
            id=uid,
            name=d["name"],
            slug=d["slug"],
            description=d["description"],
            parent_id=d["parent_id"],
            color=d["color"],
            icon=d["icon"],
            created_at=now,
        )
    return get_by_id(uid)


def get_by_id(genre_id: str) -> dict[str, object] | None:
    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            _MATCH_GENRE
            + """
RETURN properties(g) AS p, elementId(g) AS eid
LIMIT 1
""",
            id=genre_id,
        )
        record = result.single()
        if not record:
            return None
        return _row_with_id(dict(record["p"]), record["eid"])


def list_all(skip: int = 0, limit: int = 100) -> list[dict[str, object]]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            """
            MATCH (g:Genre)
            WITH g, elementId(g) AS eid,
                 coalesce(g.created_at, datetime('1970-01-01T00:00:00Z')) AS sort_ts
            ORDER BY sort_ts DESC
            SKIP $skip
            LIMIT $limit
            RETURN properties(g) AS p, eid
            """,
            skip=skip,
            limit=limit,
        )
        out: list[dict[str, object]] = []
        for record in result:
            p = dict(record["p"])
            out.append(_row_with_id(p, record["eid"]))
        return out


def update(genre_id: str, patch: GenreUpdate) -> dict[str, object] | None:
    data = patch.model_dump(exclude_unset=True)
    updates = []
    params: dict[str, object] = {"id": genre_id}
    for key in _PATCH_KEYS:
        if key not in data:
            continue
        val = data[key]
        if val is None:
            continue
        updates.append(f"g.{key} = ${key}")
        params[key] = val
    if not updates:
        return get_by_id(genre_id)
    set_clause = ", ".join(updates)
    driver = get_driver()
    with driver.session() as session:
        session.run(
            _MATCH_GENRE + f" SET {set_clause} RETURN g",
            **params,
        )
    return get_by_id(genre_id)


def delete(genre_id: str) -> None:
    driver = get_driver()
    with driver.session() as session:
        session.run(_MATCH_GENRE + " DETACH DELETE g", id=genre_id)
