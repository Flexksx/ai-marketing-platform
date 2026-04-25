# ai-marketing-platform

An AI-powered marketing platform for brand and content management. It provides tools to organize brand assets and manage content items through a structured API.

## Backend Structure

The backend is located in `backend/platform-api/` and consists of several Gradle modules:

- **platform-api-service**: The core Spring Boot application containing business logic, REST controllers, and persistence layers.
- **platform-api-client**: A library module containing shared API contracts and DTOs.

Development follows a layered architecture:
1. **Presentation (REST)**: Controllers implementing API interfaces.
2. **Service**: Business logic and domain orchestration.
3. **Persistence**: Repository-based data access.

## Development

### Common Commands

We use `just` as the primary command runner.

#### Formatting
To automatically format code using Spotless:
```bash
just format <module>
```
Supported format targets: `nix`, `platform` (both), `platform-api-client`, `platform-api-service`.

#### Linting
To run style checks:
```bash
just lint <module>
```
Supported modules: `platform` (both), `platform-api-client`, `platform-api-service`.

### Environment
The project uses **Nix** for environment management (`flake.nix`). 
- If using `direnv`, run `direnv allow`.
- Otherwise, use `nix develop` to enter the development shell.

## Docker Compose

### Build-only Compose

Use the root compose file to build backend and frontend images from their Dockerfiles:

```bash
docker compose build
```

### Development Compose (hot reload)

Use the dev compose file for local development:

```bash
docker compose -f docker-compose.dev.yml up
```

It runs:
- `backend`: JDK 25 image from `backend/platform-api/Dockerfile`, running `bootRun --continuous`
- `frontend`: image from `apps/webapp/Dockerfile`, running the webapp dev server
- `postgres`: local PostgreSQL instance for backend runtime
