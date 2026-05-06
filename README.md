# Voz AI

AI-powered marketing platform. Generates brand identities, campaign strategies, and content plans from a URL or a brief description.

## Stack

| Layer | Tech |
|---|---|
| Frontend | SvelteKit 5, Tailwind CSS v4, TanStack Query v6, bits-ui |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic AI |
| Database | PostgreSQL (Supabase) |
| Auth | Supabase Auth |
| AI | OpenAI, Google Gemini |
| Hosting | Cloudflare Pages (frontend), Docker (backend) |

## Local development

### Prerequisites

- [just](https://github.com/casey/just)
- [uv](https://github.com/astral-sh/uv)
- [pnpm](https://pnpm.io)
- Docker + Docker Compose

### Environment

Copy `.envrc.example` to `.envrc` and fill in the values:

```
PUBLIC_SUPABASE_URL=
PUBLIC_SUPABASE_PUBLISHABLE_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=postgresql://vozai:vozai_dev_password@localhost:5433/vozai_dev
DIRECT_URL=postgresql://vozai:vozai_dev_password@localhost:5433/vozai_dev
PUBLIC_BACKEND_URL=http://localhost:8000
OPENAI_API_KEY=
GEMINI_API_KEY=
```

### Commands

```bash
# Start infra (Postgres + API + Worker containers)
just dev up

# Stop infra
just dev down

# Start frontend dev server
just dev ui

# Start backend API (outside Docker, hot-reload)
just dev back

# Format frontend
just format ui

# Format backend
just format back
```

### Services

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Client API | http://localhost:8000 |
| Worker API | http://localhost:8001 |
| Container logs (Dozzle) | http://localhost:8888 |
