## MODIFIED Requirements

### Requirement: Compose image references are environment configurable
The system SHALL allow Docker Compose image references and local development startup behavior to be configured from documented environment values across runtime and development workflows.

#### Scenario: Base compose uses configured published image
- **WHEN** an operator defines image registry and tag values in the root `.env` file and starts the base Compose stack
- **THEN** Docker Compose resolves the backend runtime image reference using those values

#### Scenario: Base compose prerequisites are documented
- **WHEN** a contributor follows the repository documentation for the base Compose workflow
- **THEN** the documentation states that the workflow depends on a published image being available or on an equivalent prior local image build

#### Scenario: Development compose keeps local build workflow available
- **WHEN** a contributor starts Docker Compose with the development overlay in a local development environment
- **THEN** Docker Compose uses the defined local build configuration and development container settings for the backend and frontend services without requiring a published backend image

#### Scenario: Development compose publishes the frontend port
- **WHEN** a contributor starts Docker Compose with the development overlay
- **THEN** the frontend service is reachable from the host on the configured frontend port

#### Scenario: Full-stack development compose remains available
- **WHEN** a contributor starts Docker Compose with the development and full-stack overlays together
- **THEN** the backend, frontend, and optional mailserver services start with the documented local workflow expectations intact

#### Scenario: Compose image tags default to latest
- **WHEN** an operator starts the base Compose stack without setting an image tag
- **THEN** Docker Compose resolves backend image references using the `latest` tag
