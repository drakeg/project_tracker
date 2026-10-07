# Production Deployment

The Docker Compose configuration in this repository is intended primarily for local development. Production deployments should provide production-specific environment values and place the Django application behind a trusted TLS-terminating reverse proxy.

## Required production settings

At minimum:

```dotenv
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=<strong-random-secret>
DJANGO_ALLOWED_HOSTS=tracker.example.com
API_ALLOW_ANONYMOUS=false
```

When `DJANGO_DEBUG=false`, the application will refuse to start without `DJANGO_SECRET_KEY`. This prevents accidental use of the built-in development key.

## HTTPS and cookies

For an HTTPS deployment, enable:

```dotenv
DJANGO_SECURE_SSL_REDIRECT=true
DJANGO_SESSION_COOKIE_SECURE=true
DJANGO_CSRF_COOKIE_SECURE=true
```

If Django is behind a trusted reverse proxy that terminates TLS and sets `X-Forwarded-Proto` correctly, also enable:

```dotenv
DJANGO_TRUST_X_FORWARDED_PROTO=true
```

Do not enable that setting unless the application only accepts proxy traffic from infrastructure you trust.

## HSTS

HSTS should only be enabled after HTTPS is working correctly for the deployment.

A conservative starting point is:

```dotenv
DJANGO_SECURE_HSTS_SECONDS=3600
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=false
DJANGO_SECURE_HSTS_PRELOAD=false
```

Increase the duration only after validating the deployment. Enable subdomains or preload only when every affected hostname is permanently HTTPS-capable.

## CORS

CORS remains restrictive by default. Prefer an explicit origin allowlist:

```dotenv
DJANGO_CORS_ALLOW_ALL_ORIGINS=false
DJANGO_CORS_ALLOWED_ORIGINS=https://app.example.com
```

Do not use `DJANGO_CORS_ALLOW_ALL_ORIGINS=true` for an exposed deployment unless unrestricted browser access is an intentional requirement.

## Production readiness check

Before deploying, run:

```bash
ruff check .
ruff format --check .
python manage.py check --deploy
python manage.py makemigrations --check --dry-run
python manage.py test
```

The normal CI workflow runs the application checks and tests. A deployment pipeline should additionally run `python manage.py check --deploy` with production-like environment settings.
