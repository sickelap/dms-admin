# admin-ui-delivery Specification

## Purpose
TBD - created by archiving change unify-production-image. Update Purpose after archive.
## Requirements
### Requirement: FastAPI serves the built admin UI
The system SHALL serve the production-built admin frontend from the same FastAPI runtime that exposes the admin API.

#### Scenario: Root document requested
- **WHEN** an operator requests the admin application root from the production runtime
- **THEN** the FastAPI service returns the built admin HTML entrypoint without requiring a separate frontend container

#### Scenario: Static asset requested
- **WHEN** a browser requests a built frontend static asset from the production runtime
- **THEN** the FastAPI service returns the requested asset from the bundled frontend build output

### Requirement: Client-side admin routes resolve through the production runtime
The system SHALL support browser refresh and direct navigation for client-side admin routes served by the production runtime.

#### Scenario: Direct navigation to client route
- **WHEN** an operator requests a client-side admin route that is not an API endpoint or static asset path
- **THEN** the FastAPI service returns the built admin HTML entrypoint so the client router can resolve the route

#### Scenario: API route requested
- **WHEN** a client requests an `/api` route from the production runtime
- **THEN** the FastAPI service processes the API route normally and does not replace it with the frontend HTML entrypoint

### Requirement: Production frontend uses same-origin API access by default
The system SHALL allow the production-served frontend to call the admin API through a same-origin `/api` base path by default.

#### Scenario: Production frontend calls session endpoint
- **WHEN** the production-served frontend requests session state without an explicit API host override
- **THEN** it sends the request to the same origin under `/api`

