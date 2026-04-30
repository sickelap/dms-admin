# mail-quota-management Specification

## Purpose
TBD - created by archiving change add-dms-admin-v1. Update Purpose after archive.
## Requirements
### Requirement: Operators can view account quotas
The system SHALL provide quota information for managed accounts when quota data exists for the configured DMS instance.

#### Scenario: Quota state requested
- **WHEN** an authenticated operator requests quota information
- **THEN** the system returns the observable quota configuration for the relevant managed accounts

### Requirement: Operators can set account quotas through DMS setup
The system SHALL set account quotas using a supported DMS `setup` quota operation and SHALL report the result based on observed quota state after execution.

#### Scenario: Quota set is verified
- **WHEN** an authenticated operator sets a valid quota for an existing account
- **THEN** the system executes the supported DMS setup command and reports the quota as applied only if the resulting quota state shows the expected value for that account

### Requirement: Operators can remove account quotas through DMS setup
The system SHALL remove account quotas using a supported DMS `setup` quota removal operation and SHALL verify that the quota is no longer present afterward.

#### Scenario: Quota removal is verified
- **WHEN** an authenticated operator removes a quota from an existing account
- **THEN** the system executes the supported DMS setup command and reports the quota as removed only if the resulting quota state no longer contains that account quota entry

