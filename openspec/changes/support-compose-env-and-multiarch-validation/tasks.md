## 1. Environment And Compose Configuration

- [x] 1.1 Add a root `.env.example` documenting supported local compose settings and defaults.
- [x] 1.2 Update root compose services to load `.env` values while preserving current safe defaults.
- [x] 1.3 Update compose files for compatibility with older `docker-compose` versions.

## 2. Compose Command Compatibility

- [x] 2.1 Add compose command detection to the DMS integration test helper, preferring `docker compose` and falling back to `docker-compose`.
- [x] 2.2 Add unit coverage for compose command detection without requiring Docker to be running.

## 3. Multi-Architecture Validation Script

- [x] 3.1 Add a repository script that validates Docker and Buildx prerequisites before running platform checks.
- [x] 3.2 Build backend and frontend images for `linux/amd64` and `linux/arm64` one platform at a time.
- [x] 3.3 Run backend unit tests and frontend test/build checks inside the platform-specific images.
- [x] 3.4 Ensure missing platform support exits with an actionable error message.

## 4. Documentation And Verification

- [x] 4.1 Update README setup docs for `.env`, compose command variants, and the multi-architecture validation script.
- [x] 4.2 Run backend tests that cover compose command detection.
- [x] 4.3 Run frontend tests and build checks.
- [x] 4.4 Run or document the result of the multi-architecture validation script.
