## ADDED Requirements

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
