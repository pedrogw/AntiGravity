# Capability: api-integration

## Requirements
- MUST include tests for user registration and JWT token fetching.
- MUST validate JSON creation format for Factories and Stores.
- MUST test positive and negative scenarios (e.g., duplicated email raising 409).
- MUST run purely containerized inside api docker.

## BDD Scenarios

**GIVEN** the API is running and DB is reachable
**WHEN** the client registers a new user with valid data
**THEN** the API returns HTTP 201 Created

**GIVEN** an existing registered user
**WHEN** the client hits /auth/login with valid credentials
**THEN** it returns HTTP 200 with an `access_token` Bearer
