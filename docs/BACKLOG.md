# Prioritized Backlog

This is the source of truth for planned project work. Items should be refined
before sprint commitment and removed or marked complete when superseded.

Priority: P0 blocker/security, P1 high-value core work, P2 normal roadmap work,
P3 polish/future work. Size: S, M, L.

## Ready

### PT-103 — Add production deployment check to CI
- Priority: P1
- Size: M
- Story: As an operator, I want production-oriented Django checks in CI so that
  unsafe deployment settings are caught before release.
- Acceptance criteria:
  - CI runs `manage.py check --deploy` with production-like settings;
  - expected warnings are resolved or explicitly documented;
  - normal development CI remains green.

### PT-104 — Add API-key rotation workflow
- Priority: P1
- Size: M
- Story: As an operator, I want a safe credential rotation workflow so that a
  key can be replaced without exposing or reusing secrets.
- Acceptance criteria:
  - replacement key is issued as a new credential;
  - old key can be revoked explicitly;
  - documentation includes a no-downtime rotation sequence;
  - tests cover resulting authentication behavior.

### PT-105 — Review contact/comment/update query performance
- Priority: P2
- Size: M
- Story: As an operator, I want related list endpoints to avoid avoidable N+1
  queries so that performance remains stable as data grows.
- Acceptance criteria:
  - relevant hot paths are inspected;
  - eager loading is added only where it reduces real relationship queries;
  - regression tests cover any optimized paths.

### PT-106 — Add container healthcheck configuration
- Priority: P2
- Size: S
- Story: As an operator, I want Docker health status to use the application
  health endpoint so that container orchestration can detect unhealthy state.
- Acceptance criteria:
  - Compose healthcheck calls `/health/`;
  - startup timing avoids false failures during migrations;
  - Docker workflow validates the configuration.

## Needs refinement

### PT-201 — Environment-driven production database configuration
- Priority: P1
- Size: L
- Open questions:
  - PostgreSQL only or multiple database engines?
  - connection URL vs individual environment variables?
  - local Compose database included or external only?
- Split before sprint commitment.

### PT-202 — Production application server
- Priority: P1
- Size: M
- Open questions:
  - WSGI or ASGI target?
  - container-only deployment or broader deployment support?
- Do not replace local `runserver` behavior until production runtime is clear.

### PT-203 — API versioning strategy
- Priority: P2
- Size: M
- Open questions:
  - URL versioning vs header/media-type versioning;
  - compatibility policy for existing clients.

### PT-204 — Standard API error envelope
- Priority: P2
- Size: M
- Open questions:
  - preserve default DRF field-error shape or wrap all errors;
  - compatibility impact on clients.

### PT-205 — Developer API usage metering
- Priority: P3 / conditional
- Size: L
- Blocked by:
  - explicit product requirement for paid or metered access.

### PT-206 — Billing-provider integration
- Priority: P3 / conditional
- Size: L
- Blocked by:
  - approved billing provider and subscription model;
  - product decision that paid API access is required.

### PT-207 — Replace DRF built-in OpenAPI generator
- Priority: P3 / dependency-blocked
- Size: M
- Blocked by:
  - verified third-party schema package compatibility with the current
    Django/DRF stack.

## Completed

### PT-101 — Validate tracker relationship filter IDs
- Priority: P1
- Size: S
- Result: non-integer tracker relationship filter values return HTTP 400 while
  valid integer filters preserve existing behavior.

### PT-102 — Validate tracker date filter formats
- Priority: P1
- Size: S
- Result: malformed tracker date filters return HTTP 400 and documented
  YYYY-MM-DD values preserve existing behavior.

## Recently completed foundation

The following capabilities are already implemented and should be treated as
baseline rather than open backlog:

- authenticated REST API with developer API-key support;
- plan-based API-key throttling;
- API-key last-used auditing and command-line revocation;
- complete CRUD coverage for project models;
- tracker relationship write IDs;
- tracker filtering/search/ordering;
- comment/update filtering and search;
- API pagination;
- case-insensitive lookup duplicate validation;
- health endpoint;
- production security settings;
- Docker Compose development workflow;
- Django admin usability improvements;
- Ruff lint/format CI;
- sprint/coding/deployment/developer-access documentation.
