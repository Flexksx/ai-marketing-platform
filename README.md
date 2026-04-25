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
Supported modules: `platform` (both), `platform-api-client`, `platform-api-service`.

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
