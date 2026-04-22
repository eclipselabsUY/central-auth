# GET /health

Health check endpoint.

## Request

- Method: `GET`
- Path: `/health`
- Body: none
- Query params: none

## Response

- Status: `200 OK`
- JSON body:
  - `status` (string): health state, currently `"healthy"`
