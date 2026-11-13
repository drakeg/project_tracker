# Product Roadmap

This roadmap organizes development by outcome rather than by individual pull
request. The detailed, prioritized work lives in [BACKLOG.md](BACKLOG.md).

## Product direction

Project Tracker should be a secure, maintainable Django application with:

- a dependable REST API for tracker data;
- safe developer API access;
- predictable deployment and monitoring behavior;
- efficient list/query behavior as data grows;
- clear operational and development documentation.

Paid API access remains optional and should not be implemented until it becomes
an explicit product requirement.

## Roadmap themes

### Theme 1 — API reliability and contract quality

Goal: make API behavior predictable, validated, and easy to integrate.

Near-term outcomes:

- malformed filter values return controlled `400` responses rather than
  database/type errors;
- relationship writes and list filtering remain covered by regression tests;
- pagination, ordering, search, and error behavior stay documented;
- API-key lifecycle operations are safe and auditable.

Exit criteria:

- common invalid inputs have explicit tests;
- list endpoints have stable documented behavior;
- authentication failures do not leak credential details.

### Theme 2 — Performance and scalability

Goal: prevent query growth and response degradation as tracker data increases.

Near-term outcomes:

- tracker list/detail serialization avoids N+1 relationship queries;
- contact/comment/update list views use eager loading where nested/related data
  warrants it;
- query-count regression tests protect hot paths;
- pagination limits remain configurable and bounded.

Exit criteria:

- representative list endpoints have query-count coverage;
- query count grows primarily with pages, not rows.

### Theme 3 — Operations and production readiness

Goal: make deployments observable, repeatable, and safer.

Near-term outcomes:

- health checks cover application/database readiness;
- CI includes production-oriented Django checks;
- deployment docs clearly separate development and production settings;
- production database configuration is environment-driven;
- container startup uses an appropriate production server when production
  deployment becomes a target.

Exit criteria:

- `check --deploy` is validated under production-like settings;
- monitoring has a stable endpoint;
- secrets and secure transport settings are documented and tested.

### Theme 4 — Administration and maintainability

Goal: keep routine administration efficient without custom UI work where Django
admin already solves the problem.

Near-term outcomes:

- core models have useful admin search/filter/list views;
- API keys expose safe audit metadata;
- lookup/reference data is protected from duplicates;
- management commands cover key operational workflows.

Exit criteria:

- common operational tasks do not require direct database edits;
- admin/search workflows are covered by lightweight tests.

### Theme 5 — API platform evolution

Goal: prepare for future external integrations without prematurely adding
billing or unnecessary infrastructure.

Candidate outcomes:

- API versioning strategy;
- API-key rotation workflow;
- optional usage metering;
- billing-provider integration only when explicitly approved;
- replacement of DRF's deprecated built-in OpenAPI generator once a compatible
  option is officially supported.

## Near-term sprint sequence

### Sprint A — Performance hardening

Goal: eliminate avoidable N+1 behavior on tracker list responses.

Committed:

- optimize tracker relationship loading;
- add query-count regression coverage.

Stretch:

- review contact/comment/update query patterns for similar issues.

### Sprint B — Input validation hardening

Goal: make query/filter failures predictable for API clients.

Status: completed.

Delivered:

- relationship filter ID validation;
- strict date filter validation;
- DRF `400` responses for malformed tracker query parameters;
- documented error behavior.

### Sprint C — Production-readiness checks

Goal: catch deployment misconfiguration before release.

Planned:

- add production-like `manage.py check --deploy` CI coverage;
- document required CI environment variables;
- review Compose/Docker healthcheck integration.

### Sprint D — API-key lifecycle completion

Goal: make developer credentials manageable without direct database changes.

Planned:

- add rotation/replacement workflow;
- add explicit expiration tooling;
- document incident-response steps for compromised credentials.

## Deferred / conditional roadmap

These items are intentionally not committed:

- billing-provider integration;
- paid request metering;
- major frontend redesign;
- third-party OpenAPI migration without verified framework compatibility.

They should enter the backlog only after the product requirement or dependency
compatibility is confirmed.
