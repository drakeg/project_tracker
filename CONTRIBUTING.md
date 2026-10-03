# Contributing

## Development workflow

1. Create a focused branch from `master`.
2. Keep changes small enough to review independently.
3. Add or update tests for behavior changes.
4. Update documentation when configuration, APIs, or developer workflows change.
5. Run the same validation used by CI before opening a pull request.

## Required local checks

Run:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

For container-related changes, also run:

```bash
cp .env.example .env
docker compose config --quiet
docker compose build
```

## Pull requests

Pull requests should:

- explain the problem being solved;
- summarize the implementation;
- call out migrations or configuration changes;
- include tests for fixes and new behavior;
- avoid unrelated refactors;
- keep generated IDE/editor files out of the repository.

Branches should be deleted after merge.
