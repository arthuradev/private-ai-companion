# Scripts

Operational helper scripts may live here when a phase needs them.

Scripts must stay outside product logic. The official app entrypoint remains
the Python package declared in `pyproject.toml`.

## Current scripts

- `release-check.ps1`: runs quality checks, builds sdist/wheel artifacts and
  validates the Windows launcher diagnostics path.

Scripts may prepare, validate or package the project, but they must not contain
conversation, provider, memory, avatar, safety, skill or desktop action logic.
