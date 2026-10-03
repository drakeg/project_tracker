# project_tracker

A Django and Django REST Framework project tracker.

## Docker Compose

The recommended local setup uses Docker Compose.

1. Create your local environment file:

   ```bash
   cp .env.example .env
   ```

2. Adjust values in `.env` if needed. The application port is controlled by
   `APP_PORT`, so no Compose file edits are required:

   ```dotenv
   APP_PORT=8000
   DJANGO_SECRET_KEY=change-me-for-local-development
   DJANGO_DEBUG=true
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. Build and start the application:

   ```bash
   docker compose up --build
   ```

4. Open the application at `http://localhost:8000/projects/`, replacing
   `8000` with your configured `APP_PORT`.

The container applies the checked-in Django migrations before starting the
development server. Stop it with `Ctrl-C`, or run `docker compose down` from
another terminal.

## Local Python setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Set local configuration as needed:

   ```bash
   export DJANGO_SECRET_KEY="local-development-secret"
   export DJANGO_DEBUG=true
   export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
   ```

4. Run Django checks and tests:

   ```bash
   python manage.py check
   python manage.py makemigrations --check --dry-run
   python manage.py test
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

## API

The REST API is available under `/api/projects/`.

Current resources include:

- `/api/projects/trackers/`
- `/api/projects/contacts/`
- `/api/projects/keywords/`
- `/api/projects/status/`

OpenAPI documentation is available at:

- `/api/schema/` — machine-readable OpenAPI schema
- `/api/docs/` — interactive Swagger UI

The current implementation uses Django REST Framework's built-in OpenAPI
generator because it is compatible with the project's Django 6.1 / DRF 3.18
stack. DRF has deprecated its built-in generator in favor of third-party
schema packages, so this should be revisited when a replacement officially
supports the current framework versions.

## CORS configuration

CORS is restrictive by default.

For local development only, all origins can be enabled in `.env`:

```dotenv
DJANGO_CORS_ALLOW_ALL_ORIGINS=true
```

For an explicit allowlist instead:

```dotenv
DJANGO_CORS_ALLOWED_ORIGINS=https://example.com,https://app.example.com
```

Do not enable all origins in production.

## Development process

See:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [Coding standards](docs/CODING_STANDARDS.md)
- [Sprint process](docs/SPRINTS.md)

## Continuous integration

GitHub Actions installs dependencies, verifies Django system checks and
migrations, applies migrations, and runs the test suite on pull requests and
pushes to `master`. Docker-related changes are also validated by the Docker
workflow.
