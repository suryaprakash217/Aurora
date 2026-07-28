# Architecture

Aurora is organized around a small set of clear responsibilities:

- aurora/ contains the Python package and runtime modules.
- config/ stores default configuration values.
- tests/ covers behavior changes and regression safety.
- docs/ holds the main project guidance.

## Design goals

- Keep the UI layer separate from the core logic.
- Keep features modular and independently configurable.
- Favor explicit configuration over hard-coded behavior.
- Keep the project easy to understand for contributors.

## Repository layout

- aurora/ — implementation code and feature modules
- config/ — defaults and configuration data
- tests/ — automated tests
- docs/ — overview and contributor guidance

This structure is intentionally simple so the project can grow without becoming difficult to navigate.


---

## 6. Startup Flow

The startup sequence is intentionally linear and observable:

1. Bootstrap process begins.
2. Load configuration from the layered sources.
3. Validate configuration.
4. Initialize core services such as logging, state, and event bus.
5. Register feature services.
6. Initialize UI shell surfaces.
7. Connect features to the backend state and event system.
8. Enter the main event loop.

### Startup responsibilities

- app/bootstrap.py: entry point orchestration.
- app/lifecycle.py: manage initialization and shutdown phases.
- core/config/*: assemble configuration state.
- features/*/service.py: register each feature with the runtime.
- ui/qml/*: render the shell surfaces after services are available.

---

## 7. Dependency Graph

The dependency graph should follow a one-way design:

```text
App Bootstrap
  -> Config Loader
  -> Logging
  -> State Store
  -> Event Bus
  -> Platform Adapter
  -> Feature Services
  -> UI Bridge
  -> QML Shell
```

### Dependency rules

- Core services may depend on other core services.
- Feature services may depend on core services.
- UI components may depend on feature services and core state.
- UI components must not directly mutate core state without going through a service.
- Plugins may depend on core services and feature interfaces, but not on concrete UI implementations unless explicitly designed.

---

## 8. Naming Conventions

### Python
- Use snake_case for modules, functions, methods, and variables.
- Use PascalCase for classes.
- Use UPPER_SNAKE_CASE for constants.
- File names should reflect their purpose, not their implementation detail.

### QML
- Use PascalCase for component names.
- Use camelCase for JavaScript properties and functions.
- Keep component files focused and single-purpose.

### JSON keys
- Use lowercase snake_case.
- Group settings by feature namespace.

### Feature folders
- Use lowercase singular names.
- Example: panel/, launcher/, notifications/

### Service names
- Use suffix service where appropriate.
- Example: panel_service.py, settings_service.py

---

## 9. Coding Standards

### General
- Prefer explicit code over clever abstractions.
- Keep functions small and focused.
- Avoid hidden side effects.
- Prefer composition over inheritance.
- Keep business logic away from UI code.

### Python
- Use type hints for public APIs.
- Keep modules narrow and cohesive.
- Use docstrings for public classes and functions.
- Handle errors explicitly and report meaningful exceptions.
- Do not mix configuration, UI, and feature logic inside the same module.

### QML
- Keep QML declarative and readable.
- Move complex behavior into backend-facing helpers or Python bridge services.
- Keep visual logic minimal and maintainable.

### Testing
- Unit tests for services and pure logic.
- Integration tests for runtime orchestration.
- UI tests for critical interaction flows.

---

## 10. Documentation Standards

- Every public module must have a docstring.
- Every major subsystem must have a dedicated markdown document.
- Keep README files short and actionable.
- Use architecture docs to describe design intent, not implementation details.
- Document configuration keys and defaults in the config docs.
- Update documentation whenever behavior changes.

### Documentation files
- README.md: project overview and quick start
- docs/architecture.md: system design
- docs/configuration.md: configuration model
- docs/coding-standards.md: coding rules
- docs/naming-conventions.md: naming policy
- docs/git-workflow.md: branch and commit expectations
- docs/plugin-api.md: plugin extension contract

---

## 11. Git Workflow

The repository should follow a disciplined Git workflow:

1. Create a feature branch for each logical change.
2. Keep commits focused and atomic.
3. Use descriptive commit messages.
4. Open a pull request for review before merging.
5. Prefer small, reviewable changes over large batches.

### Commit message convention

- feat: add a new capability
- fix: repair an issue
- refactor: improve structure without behavior change
- docs: update documentation
- test: add or adjust tests
- chore: maintenance unrelated to features

### Branch naming

- feature/<short-name>
- fix/<short-name>
- refactor/<short-name>
- docs/<short-name>

---

## 12. Plugin Design Direction

Plugins should be optional add-ons that integrate through interfaces rather than hard-coded dependencies.

### Plugin contract
- A plugin exposes metadata and a registration hook.
- A plugin can register a feature service and optional UI components.
- Plugins must be able to enable and disable themselves via configuration.
- Plugins must not break the base shell if they fail to initialize.

### Plugin lifecycle
- Discover plugin manifests.
- Validate plugin metadata.
- Load plugin entry points.
- Register plugin service.
- Initialize plugin if enabled.

---

## 13. Implementation Strategy

Implementation will proceed in phases:

1. Establish the runtime and core services.
2. Implement the panel and workspace shell surfaces.
3. Add launcher and notifications modules.
4. Introduce settings and plugin registration.
5. Harden configuration, documentation, and packaging.

This phased approach keeps the architecture stable while allowing the project to grow incrementally.
