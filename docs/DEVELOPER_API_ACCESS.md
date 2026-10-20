# Developer API Access

The application supports developer API keys for third-party integrations while
keeping interactive user access available through Django REST Framework session
and basic authentication.

## Issuing a key

Create or select a Django user for the integration, then issue a key:

```bash
python manage.py create_developer_api_key \
  --username integration-user \
  --name "Example integration" \
  --plan developer
```

The plaintext key is printed once. Store it in a secrets manager or other secure
credential store. The database stores only a password-style hash plus a short,
non-secret prefix used to locate the credential.

## Using a key

Send the credential in the `X-API-Key` header:

```text
X-API-Key: ptk_<prefix>_<secret>
```

The API key authenticates as its associated Django user, so the existing DRF
`IsAuthenticated` permission continues to apply.

## Plans

Each key carries one of these plan values:

- `free`
- `developer`
- `internal`

Plan values now control request throttling for developer API keys:

- `free`: defaults to `100/hour`;
- `developer`: defaults to `1000/hour`;
- `internal`: unthrottled.

The free and developer limits are configurable with:

```dotenv
API_FREE_THROTTLE_RATE=100/hour
API_DEVELOPER_THROTTLE_RATE=1000/hour
```

Interactive session/basic-auth users are not affected by these developer-key
limits.

The application still does not collect payment or meter billable usage. A
future paywall can map successful subscription events to the `developer`
plan and deactivate or downgrade keys when a subscription expires, without
changing how clients authenticate.

## Revocation and expiration

Keys can be disabled from Django admin by clearing `is_active`. They can also
be assigned an `expires_at` value. Disabled, expired, malformed, and invalid
keys all fail authentication without revealing which part of the credential was
incorrect.

## Security properties

- plaintext keys are never stored;
- keys are generated from Python's cryptographically secure `secrets` module;
- the stored key value uses Django's password hashing framework;
- each key belongs to a Django user;
- users can have multiple independently revocable integration keys;
- free and developer plans have separate request limits;
- internal keys are not throttled by the developer-key throttles.

Billing-provider integration and billable request metering should remain
separate concerns rather than embedding payment logic into authentication.
