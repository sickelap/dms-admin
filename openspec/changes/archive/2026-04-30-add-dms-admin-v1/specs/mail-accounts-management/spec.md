## ADDED Requirements

### Requirement: Operators can list managed email accounts
The system SHALL provide a way to list DMS email accounts managed by the `FILE` provisioner for the configured server.

#### Scenario: Account list requested
- **WHEN** an authenticated operator requests the accounts view
- **THEN** the system returns the current set of managed email accounts for the configured DMS instance

### Requirement: Operators can create email accounts through DMS setup
The system SHALL create email accounts by executing the supported DMS `setup` account creation operation and SHALL report the result based on observed state after execution.

#### Scenario: Account creation is verified
- **WHEN** an authenticated operator creates a new valid email account with a password
- **THEN** the system executes the supported DMS setup command and reports the account as applied only if the created account is observable in the resulting account state

#### Scenario: Account creation conflicts with existing account state
- **WHEN** an authenticated operator attempts to create an account that already exists or otherwise violates DMS setup constraints
- **THEN** the system rejects the request without reporting the account as applied

### Requirement: Operators can reset account passwords
The system SHALL reset an account password through a supported DMS `setup` operation and MUST NOT return the submitted password in subsequent responses.

#### Scenario: Password reset succeeds
- **WHEN** an authenticated operator submits a valid password reset for an existing account
- **THEN** the system executes the supported DMS setup command and reports the action result without exposing the submitted password value

### Requirement: Operators can delete email accounts through DMS setup
The system SHALL delete email accounts by executing the supported DMS `setup` deletion operation and SHALL verify that the account is no longer present afterward.

#### Scenario: Account deletion is verified
- **WHEN** an authenticated operator deletes an existing account
- **THEN** the system executes the supported DMS setup command and reports the account as removed only if the account is no longer observable in the resulting account state

#### Scenario: Account deletion impact is surfaced
- **WHEN** an authenticated operator requests deletion of an account
- **THEN** the system informs the operator that DMS may also remove associated aliases and quota as part of account deletion behavior
