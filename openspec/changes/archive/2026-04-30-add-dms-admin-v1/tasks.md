## 1. Project Skeleton

- [x] 1.1 Create the FastAPI backend application structure with configuration loading, health endpoint, and dependency definitions for the DMS admin service.
- [x] 1.2 Create the React frontend application structure with authenticated app shell and page routing for Accounts, Aliases, Quotas, Relay, and System views.
- [x] 1.3 Add local development and container configuration to run the admin app alongside an already running DMS instance using a configured container name and admin credentials.
- [x] 1.4 Set up the test harness for TDD, including backend test tooling, frontend test tooling, and local container-backed integration test scaffolding for DMS.

## 2. Authentication And Protected Access

- [x] 2.1 Implement backend authentication using configured administrator credentials and session-based protection for admin endpoints.
- [x] 2.2 Implement frontend login flow, session bootstrap, and protected navigation for authenticated operators.
- [x] 2.3 Add tests covering successful login, rejected unauthenticated access, and non-exposure of configured credential values.

## 3. DMS Command Adapter And Verification

- [x] 3.1 Implement a closed DMS adapter layer that executes only supported `docker exec <container> setup ...` commands for V1 operations.
- [x] 3.2 Implement read models and parsers for accounts, aliases, quotas, relay configuration, and DMS connectivity checks.
- [x] 3.3 Implement verification-aware mutation result handling that returns applied, failed, or verification-failed outcomes based on observed state.
- [x] 3.4 Add backend tests for command construction, parsing, error handling, and verification status mapping.
- [x] 3.5 Add container-backed integration tests for DMS adapter read and write flows against a local DMS instance from v12 onward.

## 4. Accounts Management Slice

- [x] 4.1 Implement backend endpoints for listing, creating, deleting, and resetting passwords for DMS email accounts.
- [x] 4.2 Implement the frontend accounts page with list, create, delete, and reset-password flows, including deletion impact messaging.
- [x] 4.3 Add tests covering account success paths, conflict paths, password secrecy, and deletion verification behavior.

## 5. Alias And Quota Management Slices

- [x] 5.1 Implement backend endpoints for listing, creating, and deleting aliases with DMS constraint-aware validation and verification.
- [x] 5.2 Implement the frontend aliases page with list, create, and delete flows and clear conflict feedback.
- [x] 5.3 Implement backend endpoints for viewing, setting, and removing account quotas with verification-aware responses.
- [x] 5.4 Implement the frontend quota management UI integrated into the account workflow or a dedicated quotas view.
- [x] 5.5 Add tests covering alias verification, alias constraint failures, quota set/remove flows, and quota read behavior.

## 6. Relay And System Visibility Slices

- [x] 6.1 Implement backend endpoints for viewing relay state, adding relay domain mappings, excluding sender domains from the default relay, and adding relay authentication entries.
- [x] 6.2 Implement the frontend relay page with relay domain exclusion and relay authentication management flows that treat passwords as write-only.
- [x] 6.3 Implement backend and frontend system visibility for DMS connectivity, fresh state reads on request, and verification status display.
- [x] 6.4 Add tests covering relay verification behavior, DMS unavailable handling, and fresh system state presentation.

## 7. Finish And Validate

- [x] 7.1 Add end-to-end or integration coverage for the main authenticated operator flows across accounts, aliases, quotas, relay, and system status.
- [x] 7.2 Validate the containerized deployment path for the admin app against a running local DMS instance and document the supported V1 operational setup and test workflow.
- [x] 7.3 Review the change against the proposal and specs, then resolve any gaps before starting implementation work.
