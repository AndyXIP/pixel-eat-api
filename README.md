# Pixel Eat API

![Status](https://img.shields.io/badge/Status-Complete-success) ![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-009688?logo=fastapi&logoColor=white) ![Supabase](https://img.shields.io/badge/Supabase-2.28+-3ECF8E?logo=supabase&logoColor=white) ![Pydantic](https://img.shields.io/badge/Pydantic-2-E92063?logo=pydantic&logoColor=white) ![License](https://img.shields.io/badge/License-MIT-green)

Backend API for Pixel Eat — a mobile food-logging app where users photograph meals and overlay pixel-art ingredient sprites composed client-side. Built with FastAPI and Supabase, following a Schema / View / Service architecture with a read/write split for performance and safety.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development Notes](#development-notes)
- [Suggested Future Directions](#suggested-future-directions)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

Pixel Eat API handles all server-side business logic for the Pixel Eat mobile app. The client composes pixel-art ingredient sprites on-device; the API enforces correctness — validating ingredient seasonal availability, uploading meal photos to Supabase Storage, and evaluating badge awards on every post. Reads hit Supabase directly (RLS-enforced), keeping the API layer focused purely on writes and business rules.

---

## Features

### Posts

- **Photo Upload**: Accepts compressed meal photos and stores them in Supabase Storage
- **Ingredient Validation**: Verifies ingredient IDs exist and are currently in season
- **Vessel Type Validation**: Enforces allowed vessel types on every post
- **Expiry Logic**: Posts automatically expire 30 days after creation

### Badges

- **Seasonal Badges**: Awarded for using seasonal ingredients
- **Streak Badges**: Awarded for consecutive posting activity
- **Instant Evaluation**: Badge logic runs synchronously on every post and is returned in the response

### Auth & Security

- **JWT Authentication**: Bearer tokens issued by Supabase Auth
- **RLS Enforcement**: All direct Supabase reads respect Row-Level Security policies
- **Server-Side Validation**: Business rules are never trusted from the client

### API

- **Auto-generated Docs**: Swagger UI and ReDoc available in development
- **Health Check**: `GET /utils/health` endpoint for uptime monitoring
- **Static Assets**: Mock images served at `/images` for development

---

## Architecture

```
┌──────────────────────────────────────┐
│  Mobile Client                       │
│  (pixel-art composition on-device)   │
└────────────┬─────────────────────────┘
             │  Writes (JWT Bearer)
             ▼
┌──────────────────────────────────────┐
│  FastAPI (Pixel Eat API)             │
│  Views → Services → Schemas          │
└────────────┬─────────────────────────┘
             │  Validate + Write
             ▼
┌──────────────────────────────────────┐
│  Supabase                            │
│  Postgres (RLS) + Storage + Auth     │
└──────────────────────────────────────┘
             ▲
             │  Direct reads (RLS-enforced)
             │
       Mobile Client
```

---

## Tech Stack

- **FastAPI** — Async web framework with automatic OpenAPI docs
- **Uvicorn** — ASGI server
- **Pydantic v2** — Request/response validation and settings management
- **Supabase** — Postgres database, file storage, and authentication
- **python-jose** — JWT validation
- **python-multipart** — File upload handling
- **uv** — Fast Python package manager
- **mise** — Dev tool version manager (Python + uv)
- **Ruff** — Linter and formatter
- **ty** — Type checker

---

## Project Structure

```
pixel-eat-api/
├── .github/
│   └── workflows/
│       └── build.yml           # CI: lint, format, type check
├── assets/
│   └── images/                 # Mock images served at /images
├── src/
│   ├── main.py                 # FastAPI app init, routers, CORS
│   ├── config.py               # Pydantic settings (env vars)
│   ├── database.py             # Supabase client
│   ├── dependencies.py         # Auth dependency injection
│   ├── schemas/                # Pydantic models
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── ingredient.py
│   │   └── badge.py
│   ├── services/               # Business logic
│   │   ├── post_service.py
│   │   ├── storage_service.py
│   │   ├── badge_service.py
│   │   ├── vision_service.py
│   │   └── notification_service.py
│   └── views/                  # Route handlers (FastAPI routers)
│       ├── posts.py
│       ├── users.py
│       ├── ingredients.py
│       ├── badges.py
│       ├── feed.py
│       ├── diary.py
│       ├── events.py
│       ├── recipes.py
│       ├── profile.py
│       └── friends_mock.py
├── .env.example                # Environment variable template
├── Makefile                    # Dev commands
├── mise.toml                   # Tool versions (Python, uv)
├── pyproject.toml              # Project metadata and dependencies
├── uv.lock                     # Locked dependency graph
└── README.md
```

---

## Getting Started

**Prerequisites:** [mise](https://mise.jdx.dev/) (manages Python and uv versions automatically)

```bash
# Install mise if you don't have it
brew install mise

# From the repo root — installs Python 3.14 and uv as declared in mise.toml
mise install
```

**Install dependencies:**

```bash
uv sync
```

**Create a `.env` file** (see [Configuration](#configuration) below):

```bash
cp .env.example .env
# Fill in your Supabase credentials
```

**Start the development server:**

```bash
make run
```

The API will be available at `http://127.0.0.1:8000`

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## Configuration

All configuration is loaded from environment variables via Pydantic Settings.

| Variable | Required | Description |
|---|---|---|
| `SUPABASE_URL` | Yes | Supabase project URL (`https://your-project.supabase.co`) |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | Service role JWT for server-side operations |
| `STORAGE_BUCKET` | No | Storage bucket name (default: `posts`) |
| `BASE_URL` | No | API base URL (default: `http://127.0.0.1:8000`) |

---

## Usage

All write endpoints require a valid Supabase JWT passed as a Bearer token:

```
Authorization: Bearer <supabase-jwt>
```

**Key endpoints:**

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/utils/health` | No | Health check |
| `POST` | `/posts` | Yes | Create a post with photo + ingredients |
| `GET` | `/feed` | Yes | Get the public feed |
| `GET` | `/diary` | Yes | Get the current user's diary |
| `GET` | `/ingredients` | Yes | List available ingredients |
| `GET` | `/badges` | Yes | List earned badges |
| `GET` | `/recipes` | No | Browse recipes |
| `GET` | `/profile/{id}` | No | View a user's profile |

**POST /posts flow:**
1. Validate vessel type
2. Validate ingredient IDs and seasonal availability
3. Upload compressed photo to Supabase Storage
4. Insert post row (`expires_at = posted_at + 30 days`)
5. Insert post_ingredients rows
6. Evaluate and award badges (seasonal + streak)
7. Return post + any badges earned

---

## Development Notes

- **Read/write split**: The mobile client reads from Supabase directly (RLS-enforced); all writes go through this API for validation
- **No sprite handling**: Pixel-art composition happens entirely on-device — the backend never processes sprites
- **CORS**: Currently open (`allow_origins=["*"]`) — tighten for production
- **Mock data**: `friends_mock.py` and assets in `assets/images/` support frontend development without real data
- **CI pipeline**: Push to `main` runs Ruff (lint + format check) and ty (type check) via GitHub Actions

---

## Suggested Future Directions

- Tighten CORS to specific origins for production
- Add pagination to feed and diary endpoints
- Push notifications for badge awards and friend activity
- Rate limiting on post creation
- Background job for expiring old posts (instead of query-time filtering)
- Integration tests against a local Supabase instance
- Expand badge logic (combo badges, milestone badges)
- Admin endpoints for managing ingredients and seasonal availability

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) — Modern, fast web framework for Python
- [Supabase](https://supabase.com/) — Open source Firebase alternative
- [Pydantic](https://docs.pydantic.dev/) — Data validation using Python type hints
- [uv](https://docs.astral.sh/uv/) — Extremely fast Python package manager
- [mise](https://mise.jdx.dev/) — Polyglot dev tool version manager
- [Ruff](https://docs.astral.sh/ruff/) — Fast Python linter and formatter
