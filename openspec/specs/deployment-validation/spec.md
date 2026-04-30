# deployment-validation Specification

## Purpose
TBD - created by archiving change support-compose-env-and-multiarch-validation. Update Purpose after archive.
## Requirements
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

### Requirement: Container images can be published for a configured architecture
The system SHALL provide a repository script that builds and pushes backend and frontend runtime container images to a configured registry for a configured architecture.

#### Scenario: Image publishing succeeds with explicit configuration
- **WHEN** an operator runs the image publishing script with a configured registry, architecture, and tag
- **THEN** the script builds and pushes backend and frontend images for the configured architecture with the configured tag

#### Scenario: Image publishing defaults to latest tag
- **WHEN** an operator runs the image publishing script without setting an image tag
- **THEN** the script builds and pushes backend and frontend images tagged `latest`

#### Scenario: Image publishing loads root environment configuration
- **WHEN** an operator defines supported image publishing settings in the root `.env` file
- **THEN** the image publishing script uses those settings unless matching shell environment variables are already set

#### Scenario: Image publishing prerequisites are missing
- **WHEN** an operator runs the image publishing script without required Docker tooling or registry configuration
- **THEN** the script exits with a clear message that identifies the missing prerequisite

### Requirement: Compose image references are environment configurable
The system SHALL allow Docker Compose backend and frontend image references to be configured from environment values for registry, architecture, and tag.

#### Scenario: Compose uses configured published images
- **WHEN** an operator defines image registry, architecture, and tag values in the root `.env` file
- **THEN** Docker Compose resolves backend and frontend service image references using those values

#### Scenario: Compose image tags default to latest
- **WHEN** an operator starts Docker Compose without setting an image tag
- **THEN** Docker Compose resolves backend and frontend service image references using the `latest` tag

#### Scenario: Compose remains usable for local builds
- **WHEN** an operator starts Docker Compose in a local development environment
- **THEN** Docker Compose keeps the backend and frontend build configuration available for local image builds

