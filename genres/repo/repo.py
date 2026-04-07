import uuid
from datetime import datetime
from db.neo4j import get_driver

def create(name: str, slug: str | None = None, description: str | None = None, parent_id: str | None = None, color: str | None = None, icon: str | None = None) -> None:
    driver = get_driver()
    uid = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    with driver.session() as session:
        session.run(
            """
            CREATE (g:Genre { 
              id: $id, name: $name, slug: $slug, type: 'genre',
              description: $description, parent_id: $parent_id, 
              color: $color, icon: $icon, created_at: $created_at}) RETURN g
            """,
            id=uid,
            name=name,
            slug=slug,
            description=description,
            parent_id=parent_id,
            color=color,
            icon=icon,
            created_at=now,
        )
    return get_by_id(uid)

def get_by_id(id: str) -> None:
    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            "MATCH (g:Genre {id: $id}) RETURN g",
            id=id,
        )
        record = result.single()
        if not record:
            return None
        return dict(record["g"])

def list_all(skip: int = 0, limit: int = 100) -> list[dict[str, object]]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run(
            "MATCH (g:Genre) RETURN g ORDER BY g.created_at DESC SKIP $skip LIMIT $limit",
            skip=skip,
            limit=limit,
        )
        return [dict(record["g"]) for record in result]

def update(id: str, name: str | None = None, slug: str | None = None, description: str | None = None, parent_id: str | None = None, color: str | None = None, icon: str | None = None) -> None:
    driver = get_driver()
    updates = []
    params = {"id": id}
    if name is not None:
        updates.append("g.name = $name")
        params["name"] = name
    if slug is not None:
        updates.append("g.slug = $slug")
        params["slug"] = slug
    if description is not None:
        updates.append("g.description = $description")
        params["description"] = description
    if parent_id is not None:
        updates.append("g.parent_id = $parent_id")
        params["parent_id"] = parent_id
    if color is not None:
        updates.append("g.color = $color")
        params["color"] = color
    if icon is not None:
        updates.append("g.icon = $icon")
        params["icon"] = icon
    if not updates:
        return get_by_id(id)
    set_clause = ", ".join(updates)
    with driver.session() as session:
        session.run(f"MATCH (g:Genre {{id: $id}}) SET {set_clause} RETURN g", **params)
    return get_by_id(id)

def delete(id: str) -> None:
    driver = get_driver()
    with driver.session() as session:
        session.run("MATCH (g:Genre {id: $id}) DETACH DELETE g", id=id)