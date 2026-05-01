## 1. Compose configuration

- [x] 1.1 Update the local development Compose overlay to publish the frontend service on the configured host port.
- [x] 1.2 Remove obsolete Compose configuration that produces warnings without affecting runtime behavior.
- [x] 1.3 Adjust the base Compose workflow or its defaults so the supported local startup path is explicit and no longer presents a broken first-run experience.

## 2. Documentation alignment

- [x] 2.1 Update the README Compose section to distinguish the published-image base workflow from the local development workflow.
- [x] 2.2 Document the frontend host access behavior and any prerequisites for image-backed Compose startup.

## 3. Verification

- [x] 3.1 Run the documented local development Compose command and confirm that the API and frontend both start successfully.
- [x] 3.2 Verify the documented base Compose command or prerequisite path matches the resulting behavior after the configuration changes.
- [x] 3.3 Run the documented full-stack Compose workflow and confirm that the backend, frontend, and optional mailserver start successfully together.
