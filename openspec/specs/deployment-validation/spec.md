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
The system SHALL provide a repository script that validates the single production application image build and test behavior for both `linux/amd64` and `linux/arm64`.

#### Scenario: Multi-architecture validation succeeds
- **WHEN** a contributor runs the validation script on a host capable of building and running the target platforms
- **THEN** the script builds the production application image and runs the relevant automated checks for `linux/amd64` and `linux/arm64`

#### Scenario: Multi-architecture prerequisites are missing
- **WHEN** a contributor runs the validation script on a host that cannot build or run a target platform
- **THEN** the script exits with a clear message that identifies the missing Docker or platform prerequisite

### Requirement: Container images can be published for a configured architecture
The system SHALL provide separate repository scripts that build backend and frontend runtime container images for a configured architecture and push those tagged images to a configured registry.

#### Scenario: Image build succeeds with explicit configuration
- **WHEN** an operator runs the image build script with a configured registry, architecture, and tag
- **THEN** the script builds backend and frontend images for the configured architecture with the configured tag without pushing them

#### Scenario: Image push succeeds after local build
- **WHEN** an operator runs the image push script after the corresponding backend and frontend images have been built locally
- **THEN** the script pushes those tagged backend and frontend images to the configured registry

#### Scenario: Image scripts load root environment configuration
- **WHEN** an operator defines supported image build and push settings in the root `.env` file
- **THEN** the image scripts use those settings unless matching shell environment variables are already set

#### Scenario: Image push fails without required local tags
- **WHEN** an operator runs the image push script before the required backend and frontend images exist locally
- **THEN** the script exits with a clear message that identifies the missing local image prerequisite

#### Scenario: Image script prerequisites are missing
- **WHEN** an operator runs an image build or push script without required Docker tooling or registry configuration
- **THEN** the script exits with a clear message that identifies the missing prerequisite

### Requirement: Compose image references are environment configurable
The system SHALL allow Docker Compose backend and frontend image references to be configured from environment values for registry, architecture, and tag across runtime and development workflows.

#### Scenario: Base compose uses configured published images
- **WHEN** an operator defines image registry, architecture, and tag values in the root `.env` file and starts the base Compose stack
- **THEN** Docker Compose resolves backend and frontend service image references using those values

#### Scenario: Base compose can pull missing images
- **WHEN** an operator starts the base Compose stack without the configured backend or frontend images present locally
- **THEN** Docker Compose is able to pull the missing images from the configured registry and start the services

#### Scenario: Compose image tags default to latest
- **WHEN** an operator starts the base Compose stack without setting an image tag
- **THEN** Docker Compose resolves backend and frontend service image references using the `latest` tag

#### Scenario: Development compose keeps local build workflow available
- **WHEN** an operator starts Docker Compose in a local development environment
- **THEN** Docker Compose uses the defined local build configuration and development container settings for the backend and frontend services

### Requirement: Compose stack supports optional local mailserver
The system SHALL provide a Compose workflow that adds a local mailserver service only when the optional full-stack configuration is requested.

#### Scenario: Default compose stack excludes mailserver
- **WHEN** an operator starts the base Compose stack without the full-stack overlay
- **THEN** only the admin API and frontend services are included

#### Scenario: Full-stack compose includes mailserver
- **WHEN** an operator starts Docker Compose with the full-stack overlay
- **THEN** the mailserver service is included alongside the admin API and frontend services

#### Scenario: Full-stack compose wires API to the local mailserver
- **WHEN** an operator starts Docker Compose with the full-stack overlay
- **THEN** the API service is configured to target the Compose-managed local mailserver container by its expected container name
