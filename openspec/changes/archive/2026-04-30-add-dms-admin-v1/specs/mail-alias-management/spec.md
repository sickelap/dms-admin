## ADDED Requirements

### Requirement: Operators can list aliases
The system SHALL provide a way to list configured DMS aliases for the managed server.

#### Scenario: Alias list requested
- **WHEN** an authenticated operator requests the aliases view
- **THEN** the system returns the current configured aliases and their targets for the configured DMS instance

### Requirement: Operators can create aliases through DMS setup
The system SHALL create aliases using a supported DMS `setup` alias operation and SHALL report the result based on observed alias state after execution.

#### Scenario: Alias creation is verified
- **WHEN** an authenticated operator creates a valid alias with a valid target
- **THEN** the system executes the supported DMS setup command and reports the alias as applied only if the resulting alias state contains the expected mapping

#### Scenario: Alias creation violates DMS setup constraints
- **WHEN** an authenticated operator attempts to create an alias that conflicts with an existing account or alias according to DMS setup rules
- **THEN** the system rejects the request without reporting the alias as applied

### Requirement: Operators can delete aliases through DMS setup
The system SHALL delete aliases using a supported DMS `setup` alias deletion operation and SHALL verify that the alias is no longer present afterward.

#### Scenario: Alias deletion is verified
- **WHEN** an authenticated operator deletes an existing alias
- **THEN** the system executes the supported DMS setup command and reports the alias as removed only if the deleted alias is no longer observable in the resulting alias state
