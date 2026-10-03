# Sprint Process

This repository uses small, reviewable iterations rather than large batches of unrelated work.

## Working agreement

Each sprint should:

1. start with a concrete maintenance or feature goal;
2. include tests and documentation with the implementation;
3. keep CI green throughout development;
4. avoid mixing unrelated dependency updates with application changes;
5. end with merged code, closed stale issues, and deleted feature branches.

## Definition of done

A sprint item is complete when:

- implementation is merged to `master`;
- CI is green;
- Docker validation is green when applicable;
- migrations are committed for model changes;
- documentation reflects the current behavior;
- stale or superseded issues are updated or closed;
- the merged branch is deleted.

## Current modernization backlog

- Add a supported OpenAPI schema and API documentation UI.
- Review API authentication and authorization requirements before exposing endpoints beyond trusted environments.
- Expand API tests beyond smoke coverage.
- Add linting/formatting checks once the existing codebase is consistently formatted.
- Review model field constraints and data validation.
- Review production deployment settings separately from the local development configuration.
