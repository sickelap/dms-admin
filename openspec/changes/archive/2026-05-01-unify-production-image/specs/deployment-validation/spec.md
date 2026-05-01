## MODIFIED Requirements

### Requirement: Multi-architecture validation is automated
The system SHALL provide a repository script that validates the single production application image build and test behavior for both `linux/amd64` and `linux/arm64`.

#### Scenario: Multi-architecture validation succeeds
- **WHEN** a contributor runs the validation script on a host capable of building and running the target platforms
- **THEN** the script builds the production application image and runs the relevant automated checks for `linux/amd64` and `linux/arm64`

#### Scenario: Multi-architecture prerequisites are missing
- **WHEN** a contributor runs the validation script on a host that cannot build or run a target platform
- **THEN** the script exits with a clear message that identifies the missing Docker or platform prerequisite

### Requirement: Container images can be published for a configured architecture
The system SHALL provide repository scripts that build and push a single production application container image to a configured registry for a configured architecture.

#### Scenario: Image build succeeds with explicit configuration
- **WHEN** an operator runs the image build script with a configured registry, architecture, and tag
- **THEN** the script builds the production application image for the configured architecture with the configured tag

#### Scenario: Image push succeeds after build
- **WHEN** an operator runs the image push script after building the configured local image
- **THEN** the script pushes the production application image with the configured tag

#### Scenario: Image publication defaults to latest tag
- **WHEN** an operator runs the image build or push workflow without setting an image tag
- **THEN** the workflow uses the tag `latest`

#### Scenario: Image publication loads root environment configuration
- **WHEN** an operator defines supported image publication settings in the root `.env` file
- **THEN** the image build and push scripts use those settings unless matching shell environment variables are already set

#### Scenario: Image publication prerequisites are missing
- **WHEN** an operator runs the image build or push workflow without required Docker tooling, registry configuration, or a required local image
- **THEN** the workflow exits with a clear message that identifies the missing prerequisite

### Requirement: Compose image references are environment configurable
The system SHALL allow Docker Compose production runtime image references to be configured from environment values for registry, architecture, and tag while preserving a split local development workflow.

#### Scenario: Compose uses configured published image
- **WHEN** an operator defines image registry, architecture, and tag values in the root `.env` file
- **THEN** Docker Compose resolves the production runtime service image reference using those values

#### Scenario: Compose image tags default to latest
- **WHEN** an operator starts the production runtime Compose workflow without setting an image tag
- **THEN** Docker Compose resolves the production runtime service image reference using the `latest` tag

#### Scenario: Compose remains usable for local development
- **WHEN** an operator starts Docker Compose in a local development environment
- **THEN** Docker Compose keeps separate API and frontend development build configuration available for local iteration
