# Coding Standards

## Python and Django

- Follow PEP 8 and use four spaces for indentation.
- Ruff is the automated Python linter and formatter.
- Run `ruff check .` and `ruff format --check .` before opening a pull request.
- Prefer clear names over abbreviations.
- Keep view, serializer, and model responsibilities separated.
- Avoid debug `print()` calls in committed application code.
- Treat Django migrations as source code and commit them with model changes.
- Use environment variables for secrets and environment-specific configuration.
- Keep `DEBUG` disabled by default.
- Default CORS to restrictive behavior.

## API changes

- Preserve backwards compatibility unless a breaking change is intentional and documented.
- Add regression tests for every bug fix.
- Test create, read, update, and delete behavior when modifying writable serializers or viewsets.
- Validate nullable and optional fields explicitly.
- Avoid accidental upsert behavior unless the endpoint is documented to support it.

## Dependencies

- Prefer supported runtime and dependency versions.
- Remove obsolete dependencies when their features are removed.
- Let Renovate/Dependabot handle routine upgrades, but verify CI before merge.
- Resolve security findings by upgrading or removing the vulnerable dependency path rather than suppressing valid findings.
- Keep development-only tools in `requirements-dev.txt`.

## Docker

- Use Docker Compose for local container testing.
- All configurable ports and environment-specific values must be settable through `.env`.
- Keep `.env.example` current and free of secrets.
- Docker builds must be validated in CI.

## Tests and CI

At minimum, pull requests should pass:

```bash
ruff check .
ruff format --check .
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate --noinput
python manage.py test
```

Container changes must also pass the Docker workflow.
