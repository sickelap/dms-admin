## ADDED Requirements

### Requirement: Compose services load documented environment values
The system SHALL provide a documented root `.env` workflow for local compose deployments of the admin API and frontend.

#### Scenario: Compose deployment uses local environment file
- **WHEN** an operator defines supported admin application settings in the root `.env` file
- **THEN** the compose-managed API and frontend services receive those settings at runtime

#### Scenario: Compose deployment works without local environment file
- **WHEN** an operator starts the root compose deployment without a root `.env` file
- **THEN** the compose-managed services use safe documented local defaults

### Requirement: Compose configuration supports legacy compose installations
The system SHALL keep local compose configuration and test helpers usable with both the modern `docker compose` plugin and the legacy `docker-compose` binary.

#### Scenario: Modern compose plugin is available
- **WHEN** the DMS integration test harness starts or stops the local DMS container on a host with `docker compose`
- **THEN** it uses the modern compose plugin successfully

#### Scenario: Only legacy compose binary is available
- **WHEN** the DMS integration test harness starts or stops the local DMS container on a host with `docker-compose` but without `docker compose`
- **THEN** it uses the legacy compose binary successfully

### Requirement: Multi-architecture validation is automated
The system SHALL provide a repository script that validates backend and frontend container build and test behavior for both `linux/amd64` and `linux/arm64`.

#### Scenario: Multi-architecture validation succeeds
- **WHEN** a contributor runs the validation script on a host capable of building and running the target platforms
- **THEN** the script builds backend and frontend images and runs the relevant automated checks for `linux/amd64` and `linux/arm64`

#### Scenario: Multi-architecture prerequisites are missing
- **WHEN** a contributor runs the validation script on a host that cannot build or run a target platform
- **THEN** the script exits with a clear message that identifies the missing Docker or platform prerequisite
