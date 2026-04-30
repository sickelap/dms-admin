# mail-relay-management Specification

## Purpose
TBD - created by archiving change add-dms-admin-v1. Update Purpose after archive.
## Requirements
### Requirement: Operators can view relay configuration managed by setup
The system SHALL provide the current relay domain and relay authentication configuration that is managed through supported DMS `setup` operations.

#### Scenario: Relay configuration requested
- **WHEN** an authenticated operator requests relay configuration
- **THEN** the system returns the observable relay domain mappings and relay authentication entries for the configured DMS instance

### Requirement: Operators can manage relay domains through DMS setup
The system SHALL add relay domain mappings and exclude sender domains from the default relay using supported DMS `setup relay` operations and SHALL report results based on observed resulting state.

#### Scenario: Relay domain add is verified
- **WHEN** an authenticated operator adds a relay mapping for a sender domain
- **THEN** the system executes the supported DMS setup command and reports the relay mapping as applied only if the resulting relay configuration contains the expected domain entry

#### Scenario: Relay domain exclusion is verified
- **WHEN** an authenticated operator excludes a sender domain from the default relay
- **THEN** the system executes the supported DMS setup command and reports the relay exclusion as applied only if the resulting relay configuration shows that domain as excluded

### Requirement: Operators can manage relay authentication through DMS setup
The system SHALL add relay authentication entries using supported DMS `setup relay` operations and SHALL treat submitted relay passwords as write-only secrets.

#### Scenario: Relay authentication add is verified
- **WHEN** an authenticated operator adds relay authentication for a sender domain
- **THEN** the system executes the supported DMS setup command and reports the relay authentication as applied only if the resulting relay configuration contains the expected domain authentication entry without returning the submitted password

