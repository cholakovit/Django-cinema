# Django Cinema

JSON API for a movie graph catalog: titles, genres, and related entities. **Django REST Framework** exposes JSON endpoints; **Neo4j** stores the graph; request/response validation uses **Pydantic** DTOs.

## Requirements

- Python 3.13+
- Neo4j (local or AuraDB)
- [uv](https://docs.astral.sh/uv/) (recommended)

## Setup

```bash
uv sync
cp .env.example .env
```

Edit `.env` with your Neo4j URI, user, and password. Optional Django vars:

| Variable | Purpose |
|----------|---------|
| `NEO4J_URI` | e.g. `bolt://localhost:7687` |
| `NEO4J_USER` / `NEO4J_PASSWORD` | Neo4j credentials |
| `DJANGO_SECRET_KEY` | Secret key (set a strong value in production) |
| `DJANGO_DEBUG` | `0` or `false` in production |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts, e.g. `yourapp.onrender.com` |

## Run locally

```bash
uv run python manage.py runserver
```

API base path: `/api/v1/` (see `config/urls.py`).

## Deploy

1. Push this repo to GitHub.
2. On **Railway**, **Render**, or similar: connect the repo, set root to this project if it lives in a monorepo, add the same environment variables as in `.env.example`.
3. Build: `pip install -r requirements.txt` (generated with `uv export`; or `uv sync` if the host has `uv`).
4. Start: use the `Procfile` (`web:`). The platform must set `PORT` (e.g. Railway, Render).

Ensure Neo4j is reachable from the host (AuraDB URI, or a private network).

---

## Domain model (schema notes)

movie, person, genre, studio, publisher

MOVIE
Attribute	Type	Required	Notes
id	string (UUID)	yes	Unique identifier
name	string	yes	Title
type	enum	yes	movie or book
year	int	no	Release year
description	string	no	Summary / blurb
rating	float	no	0–10 or similar
created_at	datetime	yes	Created timestamp

ACTORS
Attribute	Type	Required	Notes
id	string (UUID)	yes	Unique identifier
name	string	yes	Full name
birth_year	int	no	Birth year
bio	string	no	Short biography
created_at	datetime	yes	Created timestamp

GENRE
Attribute	Type	Required	Notes
id	string (UUID)	yes	Unique identifier
name	string	yes	e.g. Action, Thriller
slug	string	no	URL-friendly key, e.g. sci-fi
description	string	no	Short description
parent_id	string	no	For hierarchies (e.g. Sci‑Fi → Cyberpunk)
color	string	no	Hex for UI badges, e.g. #FF5733
icon	string	no	Icon class or asset path
created_at	datetime	yes	Creation time

PUBLISHER
Attribute	Type	Required	Notes
id	string (UUID)	yes	Unique identifier
name	string	yes	Studio name
founded_year	int	no	Year founded
slug	string	no	URL-friendly key
country	string	no	e.g. USA, Japan
headquarters	string	no	City or location
website	string	no	Official URL
description	string	no	Short description
logo_url	string	no	Logo image URL
parent_id	string	no	For conglomerates (e.g. Warner Bros → Warner Bros Pictures)
created_at	datetime	yes	Creation timestamp


Relationships (with properties)

Relationship	From	To	Properties
ACTED_IN	Person	Movie	role (string)
DIRECTED	Person	Movie	—
WROTE	Person	Book	—
BELONGS_TO_GENRE	Title	Genre	—
PRODUCED_BY	Movie	Studio	—
PUBLISHED_BY	Book	Publisher	—
SIMILAR_TO	Title	Title	score (float, 0–1)
ADAPTED_FROM	Movie	Book	—
