### Improvements roadmap

Use this checklist to track architectural and codebase improvements. Items marked [x] are implemented.

#### Repository hygiene
- [x] Remove tracked `__pycache__` and other ignored artifacts from VCS
- [x] Keep `.gitignore` authoritative for config/output/venv artefacts
- [x] Add `.pre-commit-config.yaml` with checks (ruff, mypy, basic hooks)
- [ ] Enable pre-commit for contributors (`pre-commit install` in local clones)
- [x] Delete stray script `Demo_Roskvartal/2ch_wav/process_dialogues.py`
- [x] Audit `SPK-13769/` assets and remove if unused

#### Packaging & distribution
- [x] Standardize on Hatchling in `pyproject.toml` (remove Setuptools stanza)
- [x] Add console script entry-point `audiogram` → `clients.main:main`
- [x] Declare `ffmpeg-python` runtime dependency for `audio_converter.py`
- [x] Add `dev` optional extra (ruff, mypy, pytest, pre-commit)
- [x] Ensure wheel build includes `clients/` via Hatch build config
- [x] Restructure package names (expose library as `audiogram_client`, keep CLI as `audiogram_cli`) and update imports

#### Documentation
- [x] Update README to prefer `audiogram` CLI over `python -m clients.main`
- [x] Split docs into `docs/quickstart.md`, `docs/cli.md`, `docs/architecture.md`
- [ ] Auto-generate CLI reference (e.g., via `sphinx-click` or scripted `--help` dumps)

#### Code organisation & quality
- [x] Consolidate shared Click options into `clients/common_utils/cli_options.py`
- [x] Introduce `ModelService` abstraction and wire a comprehensive `models info` command
- [x] Replace `print` with `logging` in `audio_converter.py` and other CLIs, add `--verbose`
- [x] Move shared enums/types from service-specific utils into `clients/common_utils/types.py`
- [x] Remove commented-out code and dead exports across the repo

#### Testing & CI
- [x] Add pytest configuration (via `pyproject.toml`)
- [x] Add ruff and mypy configuration (strict defaults)
- [ ] Add initial test suite:
  - [x] CLI smoke tests with `CliRunner`
  - [ ] Config validation tests
  - [ ] Proto round-trip tests
- [x] Set up GitHub Actions workflow: lint (ruff), type-check (mypy), tests (pytest)

#### Proto management
- [x] Add regeneration script/task for `clients/genproto` from `proto/` (pin protoc/protobuf versions)
- [x] Document regeneration process in `docs/architecture.md`

#### Configuration & security
- [x] Ensure `config.ini` is ignored by default
- [ ] Review auth/config flows; consider optional environment variable support for CI

#### Developer experience
- [x] Add `.editorconfig` for consistent formatting across editors
- [x] Provide `Makefile` or `invoke` tasks for common operations (lint, test, proto-gen, docs)

---

### Recently completed (implemented in this iteration)
- Removed tracked `__pycache__` entries and committed cleanup
- Switched to Hatch-only packaging; added `audiogram` console script
- Declared `ffmpeg-python` dependency and added `dev` extras
- Added ruff, mypy configs; pytest config in `pyproject.toml`
- Added `.pre-commit-config.yaml` and `.editorconfig`
- Updated README to use `audiogram` CLI and trimmed deprecated examples


