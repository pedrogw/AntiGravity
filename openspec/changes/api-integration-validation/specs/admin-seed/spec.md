# Capability: admin-seed

## Requirements
- MUST provide an entry level script to bootstrap a pristine environment.
- MUST seed an admin user with fixed login `admin@antigravity.com` / `admin`.

## BDD Scenarios

**GIVEN** the Docker environment is fresh
**WHEN** the operator invokes the admin seed script
**THEN** the system prints "Admin Seeding completed!"
**AND** the credentials work perfectly in the Swagger UI POST /auth/login
