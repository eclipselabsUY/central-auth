# Eclipse Labs Auth Documentation

This documentation describes the current behavior of the `central-auth` service.

## Scope

- Request and response expectations for each endpoint.
- Standard HTTP errors and custom auth error codes.
- Custom exception classes used by login validation.

## Base URLs

- Production: `https://auth.eclipselabs.com.uy`
- Local development example: `http://localhost:8000`

## Current API Surface

- `GET /` - redirect to Eclipse Labs website.
- `GET /health` - service health check.
- `POST /login` - user authentication endpoint.
