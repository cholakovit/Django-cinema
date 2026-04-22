import os
from functools import lru_cache

from neo4j import GraphDatabase


@lru_cache(maxsize=1)
def get_driver():
    uri = os.environ.get("NEO4J_URI", "").strip()
    user = os.environ.get("NEO4J_USER", "").strip()
    password = os.environ.get("NEO4J_PASSWORD", "").strip()
    if not uri:
        raise RuntimeError("NEO4J_URI is not set")
    return GraphDatabase.driver(uri, auth=(user, password))
