# project_tracker

A Django and Django REST Framework project tracker.

## Local setup

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

API documentation is exposed at `/api/docs/`.

## CORS configuration

CORS is restrictive by default.

For local development only, all origins can be enabled with:

```bash
export DJANGO_CORS_ALLOW_ALL_ORIGINS=true
```

For an explicit allowlist instead:

```bash
export DJANGO_CORS_ALLOWED_ORIGINS="https://example.com,https://app.example.com"
```

Do not enable all origins in production.

## Continuous integration

GitHub Actions installs the application dependencies, runs `python manage.py check`,
and executes the Django test suite for pull requests and pushes to `master`.
