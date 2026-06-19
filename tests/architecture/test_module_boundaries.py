from __future__ import annotations

import ast
from pathlib import Path

PACKAGE_ROOT = Path("src/private_ai_companion")

FORBIDDEN_CORE_IMPORT_PREFIXES = (
    "private_ai_companion.avatar",
    "private_ai_companion.desktop",
    "private_ai_companion.speech",
    "private_ai_companion.ui",
    "private_ai_companion.vision",
)


def imported_modules(path: Path) -> set[str]:
    modules: set[str] = set()
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            modules.add(node.module)

    return modules


def test_core_does_not_import_forbidden_boundary_modules() -> None:
    core_paths = sorted((PACKAGE_ROOT / "core").rglob("*.py"))

    violations = {
        str(path): sorted(
            module
            for module in imported_modules(path)
            if module.startswith(FORBIDDEN_CORE_IMPORT_PREFIXES)
        )
        for path in core_paths
    }
    violations = {path: modules for path, modules in violations.items() if modules}

    assert violations == {}
