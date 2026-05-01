## 1. Compose Restructure

- [x] 1.1 Refactor the root Compose configuration into a runtime-oriented base file for the API and frontend image workflow.
- [x] 1.2 Add a development Compose overlay that restores local build settings, bind mounts, and dev commands for the API and frontend.
- [x] 1.3 Add a full-stack Compose overlay that introduces the optional mailserver service and wires the API to it.

## 2. Image Script Split

- [x] 2.1 Refactor shared image configuration and prerequisite checks so build and push scripts use the same environment contract.
- [x] 2.2 Update the build script so it builds backend and frontend images without pushing them.
- [x] 2.3 Add a push script that validates the required local tags and then pushes backend and frontend images to the configured registry.

## 3. Validation And Documentation

- [x] 3.1 Update automated tests or test helpers to reflect the layered Compose workflow and separate image scripts.
- [x] 3.2 Update `.env.example` and `README.md` with the new Compose command matrix and image build/push guidance.
- [x] 3.3 Manually verify or document verification for base runtime mode, development mode, and full-stack mode including pull-friendly base `docker compose up`.
