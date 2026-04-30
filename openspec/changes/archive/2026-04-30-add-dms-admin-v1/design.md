## Context

This change introduces a greenfield admin application for a single Docker Mail Server instance that is already running and uses the default `FILE` provisioner. The application will run alongside DMS as another container and will manage only operations that DMS officially exposes through its `setup` CLI.

The main constraint is trustworthiness: the admin app must not report success based only on command exit status when observed state has not been confirmed. The product must also avoid expanding into unsupported low-level configuration editing, lifecycle orchestration, or multi-server control during V1.

## Goals / Non-Goals

**Goals:**
- Provide a small but complete V1 admin interface for accounts, aliases, quotas, relay settings, and system visibility.
- Execute writes only through a closed set of DMS `setup` commands against one configured DMS container.
- Read back resulting state after mutations and expose whether a requested change was verified as applied.
- Keep the architecture simple enough to implement incrementally with a FastAPI backend and React frontend.
- Support a single-admin authentication model suitable for an internal operations tool.
- Drive implementation through TDD, with fast automated tests around backend and frontend behavior plus integration coverage against a local DMS container.

**Non-Goals:**
- Support arbitrary DMS config file editing.
- Support regex aliases, LDAP provisioners, or multiple mail servers.
- Restart, reload, or otherwise manage the DMS container lifecycle.
- Expose a generic shell execution API or unrestricted Docker control.
- Provide full mailserver observability such as message tracing, queue management, or log exploration in V1.

## Decisions

### Use a sidecar API plus web UI architecture

The system will consist of a FastAPI backend and React frontend running as a companion service next to the DMS container.

Rationale:
- Matches the deployment model the user wants.
- Keeps privileged DMS interaction on the server side.
- Separates operator UX from command execution and verification logic.

Alternatives considered:
- A frontend-only app was rejected because DMS interaction requires privileged host access.
- A CLI-only wrapper was rejected because it does not satisfy the UI requirement.

### Restrict all writes to supported `setup`-managed operations

All mutating backend operations will map to a fixed set of supported `docker exec <dms-container> setup ...` commands. The API will not write DMS config files directly in V1.

Rationale:
- Aligns with DMS-supported workflows.
- Reduces the chance of invalid or partially applied state.
- Avoids owning low-level config semantics that DMS may change across versions.

Alternatives considered:
- Direct config file editing was rejected for V1 because it would require custom validation, service reload decisions, and more fragile verification behavior.

### Model success as verified observed state, not command completion

Every mutating action will follow this pattern:
1. Execute the supported DMS command.
2. Read back the relevant resulting state.
3. Return `applied`, `failed`, or `verification_failed` based on observed state.

Rationale:
- Satisfies the requirement that the admin app confirms DMS picked up the change.
- Prevents the UI from overstating success when command output is incomplete or ambiguous.

Alternatives considered:
- Trusting exit code alone was rejected because it does not prove the requested state is observable after the change.

### Use a closed DMS adapter layer

The backend will isolate all DMS interactions inside a dedicated adapter/service layer responsible for command building, execution, parsing, and verification.

Rationale:
- Prevents shell behavior from leaking into API routes.
- Keeps the set of allowed operations auditable and testable.
- Makes it easier to swap command parsing details without changing API contracts.

Alternatives considered:
- Executing shell commands directly from route handlers was rejected because it spreads privileged behavior across the codebase and makes validation harder.

### Keep authentication intentionally simple for V1

V1 will support a single-admin login flow with credentials sourced from environment variables or mounted secrets, plus session-based authentication for the web UI.

Rationale:
- Sufficient for an internal single-operator tool.
- Avoids bringing in external identity dependencies before the core management surface is proven.

Alternatives considered:
- No authentication was rejected because the app controls sensitive mailserver operations.
- Full SSO/OIDC was rejected as unnecessary scope for V1.

### Present the UI as task-oriented management pages

The frontend will organize around operational tasks: Accounts, Aliases, Quotas, Relay, and System.

Rationale:
- Matches how operators think about DMS setup-managed actions.
- Keeps navigation and implementation straightforward.
- Avoids a misleading abstraction that implies broader DMS coverage than V1 actually provides.

Alternatives considered:
- A raw command console was rejected because it undermines validation and operator safety.
- A file-oriented UI was rejected because V1 is deliberately not config-file-first.

### Make TDD and local integration testing part of the implementation contract

Implementation will be driven by tests written ahead of feature code, using a layered test strategy:
- unit tests for command construction, parsing, validation, and verification status behavior
- API and UI tests for authenticated operator flows
- integration tests against a local DMS container for the supported `setup`-managed operations

Rationale:
- The DMS adapter is the riskiest part of the design and benefits from executable examples before implementation.
- Integration coverage is necessary because command semantics and observed state verification depend on a real DMS instance.
- A layered test strategy keeps the inner loop fast while still validating the end-to-end contract.

Alternatives considered:
- Relying only on mocked tests was rejected because it would not prove compatibility with real DMS behavior.
- Relying only on end-to-end integration tests was rejected because it would slow iteration and make failures harder to localize.

## Risks / Trade-offs

- [DMS command output may vary by version] → Keep parsing centralized, support DMS versions from v12 onward, and favor read-back verification over brittle stdout parsing.
- [Some setup-managed reads may not have a single canonical command] → Combine command output with config-backed read models where necessary, but keep writes `setup`-only.
- [The admin container needs privileged access to interact with DMS] → Limit the backend to a closed set of supported operations and never expose arbitrary command execution.
- [Verification may be incomplete for some edge cases] → Return an explicit `verification_failed` state instead of silently reporting success.
- [Single-admin auth is weaker than centralized identity] → Document the deployment assumption that V1 is an internal tool and make stronger auth a future enhancement.
- [Integration tests may be slower or more brittle than unit tests] → Keep the majority of coverage in fast unit and API tests, and reserve container-backed tests for the supported DMS contract.

## Migration Plan

1. Deploy the admin container alongside an already running DMS instance.
2. Configure the admin app with the DMS container name and authentication secrets.
3. Validate DMS reachability and supported command execution through the system status page or health endpoint.
4. Roll out account, alias, quota, and relay management to operators.

Rollback:
- Stop or remove the admin container. No DMS-specific schema or service migration is required because V1 changes DMS only through supported operational commands.

## Open Questions

- Relay exclusion support is not required for V1 unless a concrete operator need appears during implementation.
- Recent admin state should be read fresh on request instead of relying on stored action history.
- V1 should explicitly support and test DMS versions from v12 onward.
