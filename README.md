# Aurora

Aurora is a modular desktop shell project for Hyprland on Arch Linux. The repository currently contains the project foundation, configuration structure, and documentation for future development.

## What is in this repository

- aurora/ — Python package and core shell modules
- config/ — default configuration files
- tests/ — test coverage for the current implementation
- docs/ — concise project documentation

## Quick start

1. **Review the documentation** in [docs/](docs/).
2. **Install the package** in editable mode:
   ```bash
   pip install -e .
   ```
3. **Run the shell CLI**:
   ```bash
   aurora-shell
   ```
   You can also specify a custom configuration file:
   ```bash
   aurora-shell --config path/to/config.json
   ```
   Or display version and help info:
   ```bash
   aurora-shell --version
   aurora-shell --help
   ```
4. Run the test suite:
   ```bash
   pytest
   ```

## Documentation

- [docs/architecture.md](docs/architecture.md) — overall structure and design goals
- [docs/developer-guide.md](docs/developer-guide.md) — workflow for contributors
- [docs/user-guide.md](docs/user-guide.md) — high-level user overview
- [docs/configuration-guide.md](docs/configuration-guide.md) — configuration conventions

## License

Aurora is intended for release under the MIT License.
