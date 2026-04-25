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
- Entering the shell creates root-level symlinks for IDE toolchain paths:
  - `.nix-java-home`
  - `.nix-nodejs`
  - `.nix-pnpm`

## Docker Compose

### Build-only Compose

Use the root compose file to build backend and frontend images from their Dockerfiles:

```bash
docker compose build
```

### Development Compose (hot reload)

Use `just dev` targets for local development:

```bash
just dev up platform
just dev up webapp
just dev up all
```

To stop the same targets:

```bash
just dev down platform
just dev down webapp
just dev down all
```

Compose split:
- `backend/docker-compose.dev.yml`: `backend` and `postgres` services for platform API development.
- `docker-compose.dev.yml`: `frontend` service for webapp development.

`platform-api-service` disables Spring Boot's Docker Compose lifecycle by default (`SPRING_DOCKER_COMPOSE_ENABLED=false`) because `just dev` already manages containers. Set `SPRING_DOCKER_COMPOSE_ENABLED=true` only when running the service standalone and you want Spring to manage `compose.yaml`.

When `just dev up platform` is running, OpenAPI client generation is automatic:
- backend changes under `backend/platform-api/platform-api-client` or `backend/platform-api/platform-api-service` trigger OpenAPI spec regeneration.
- endpoint client classes in `lib/platform-api-client/src/generated` are regenerated from the refreshed spec.
