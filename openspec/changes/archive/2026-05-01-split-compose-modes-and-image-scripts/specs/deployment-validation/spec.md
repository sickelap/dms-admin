## MODIFIED Requirements

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
- **WHEN** an operator starts Docker Compose with the development overlay in a local development environment
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
