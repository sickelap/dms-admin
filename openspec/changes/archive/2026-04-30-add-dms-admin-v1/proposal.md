## Why

Docker Mail Server exposes day-to-day administration through its `setup` CLI, but that interface is operationally awkward for routine account management and easy to misuse. A focused admin application is needed to manage a single running DMS instance through supported `setup` operations while confirming that requested changes were actually applied.

## What Changes

- Add a FastAPI backend and React frontend for a single Docker Mail Server instance running alongside the app as another container.
- Support V1 account operations backed by DMS `setup` commands: list, create, delete, and reset password.
- Support V1 alias operations backed by DMS `setup` commands: list, create, and delete.
- Support V1 quota operations backed by DMS `setup` commands: view, set, and remove account quotas.
- Support V1 relay operations backed by DMS `setup` commands: list relay configuration, add relay domains, add relay authentication entries, and exclude sender domains from the default relay.
- Add admin authentication for a single operator session model.
- Add system status, action result visibility, and read-after-write verification so the UI reports observed applied state instead of only command success.
- Implement the change test-first, with automated unit coverage around command handling and integration coverage against a local DMS container.
- Exclude arbitrary config file editing, lifecycle management, regex aliases, and non-`FILE` provisioners from V1.

## Capabilities

### New Capabilities
- `admin-access`: Authenticate an operator before allowing access to the admin interface.
- `mail-accounts-management`: Manage DMS email accounts through supported `setup` operations.
- `mail-alias-management`: Manage DMS aliases through supported `setup` operations.
- `mail-quota-management`: Manage DMS account quotas through supported `setup` operations.
- `mail-relay-management`: Manage DMS relay domain and relay authentication settings through supported `setup` operations.
- `dms-system-observability`: Show DMS connectivity, recent action outcomes, and verification status for admin-triggered changes.

### Modified Capabilities

None.

## Impact

- New backend API service in Python with FastAPI.
- New frontend admin interface in React.
- A DMS command adapter layer that executes a closed set of `docker exec <container> setup ...` commands.
- Verification logic that reads back observed state after mutations.
- Container deployment and local development configuration for the admin app alongside a running DMS instance.
- Automated test infrastructure for TDD and local integration testing with DMS.
