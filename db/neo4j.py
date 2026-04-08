import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        user = (os.getenv("NEO4J_USER") or "neo4j").strip()
        password = (os.getenv("NEO4J_PASSWORD") or "").strip()
        uri = (os.getenv("NEO4J_URI") or "bolt://localhost:7687").strip()
        _driver = GraphDatabase.driver(uri, auth=(user, password))
    return _driver


def close_driver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
