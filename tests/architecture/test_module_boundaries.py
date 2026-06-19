from __future__ import annotations

import ast
from pathlib import Path

PACKAGE_ROOT = Path("src/private_ai_companion")

FORBIDDEN_CORE_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.avatar",
    "private_ai_companion.desktop",
    "private_ai_companion.safety",
    "private_ai_companion.speech",
    "private_ai_companion.ui",
    "private_ai_companion.vision",
)

FORBIDDEN_UI_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.core",
    "private_ai_companion.desktop",
    "private_ai_companion.memory",
    "private_ai_companion.safety",
    "private_ai_companion.skills",
    "private_ai_companion.speech",
    "private_ai_companion.vision",
)

FORBIDDEN_BRAIN_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.avatar",
    "private_ai_companion.desktop",
    "private_ai_companion.safety",
    "private_ai_companion.speech",
    "private_ai_companion.ui",
    "private_ai_companion.vision",
)

FORBIDDEN_CONFIG_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.avatar",
    "private_ai_companion.desktop",
    "private_ai_companion.safety",
    "private_ai_companion.speech",
    "private_ai_companion.ui",
    "private_ai_companion.vision",
)

FORBIDDEN_MEMORY_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.avatar",
    "private_ai_companion.brain",
    "private_ai_companion.desktop",
    "private_ai_companion.speech",
    "private_ai_companion.ui",
    "private_ai_companion.vision",
)

FORBIDDEN_SPEECH_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.brain",
    "private_ai_companion.desktop",
    "private_ai_companion.memory",
    "private_ai_companion.ui",
    "private_ai_companion.vision",
)

FORBIDDEN_AVATAR_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.brain",
    "private_ai_companion.desktop",
    "private_ai_companion.memory",
    "private_ai_companion.speech",
    "private_ai_companion.ui",
    "private_ai_companion.vision",
)

FORBIDDEN_VISION_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.avatar",
    "private_ai_companion.brain",
    "private_ai_companion.desktop",
    "private_ai_companion.memory",
    "private_ai_companion.safety",
    "private_ai_companion.skills",
    "private_ai_companion.speech",
    "private_ai_companion.ui",
)

FORBIDDEN_SAFETY_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.avatar",
    "private_ai_companion.brain",
    "private_ai_companion.desktop",
    "private_ai_companion.memory",
    "private_ai_companion.skills",
    "private_ai_companion.speech",
    "private_ai_companion.ui",
    "private_ai_companion.vision",
)

FORBIDDEN_DESKTOP_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.avatar",
    "private_ai_companion.brain",
    "private_ai_companion.memory",
    "private_ai_companion.skills",
    "private_ai_companion.speech",
    "private_ai_companion.ui",
    "private_ai_companion.vision",
)

FORBIDDEN_SKILLS_IMPORT_PREFIXES = (
    "private_ai_companion.adapters",
    "private_ai_companion.avatar",
    "private_ai_companion.brain",
    "private_ai_companion.desktop",
    "private_ai_companion.memory",
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
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "core",
        FORBIDDEN_CORE_IMPORT_PREFIXES,
    )

    assert violations == {}


def test_ui_uses_public_bootstrap_instead_of_core_or_providers() -> None:
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "ui",
        FORBIDDEN_UI_IMPORT_PREFIXES,
    )

    assert violations == {}


def test_brain_does_not_import_runtime_edges_or_safety_policy() -> None:
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "brain",
        FORBIDDEN_BRAIN_IMPORT_PREFIXES,
    )

    assert violations == {}


def test_config_does_not_import_runtime_edges() -> None:
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "config",
        FORBIDDEN_CONFIG_IMPORT_PREFIXES,
    )

    assert violations == {}


def test_memory_does_not_import_runtime_edges_or_brain() -> None:
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "memory",
        FORBIDDEN_MEMORY_IMPORT_PREFIXES,
    )

    assert violations == {}


def test_speech_does_not_import_runtime_edges_or_memory() -> None:
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "speech",
        FORBIDDEN_SPEECH_IMPORT_PREFIXES,
    )

    assert violations == {}


def test_avatar_does_not_import_runtime_edges_or_brain() -> None:
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "avatar",
        FORBIDDEN_AVATAR_IMPORT_PREFIXES,
    )

    assert violations == {}


def test_vision_does_not_import_runtime_edges_or_brain() -> None:
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "vision",
        FORBIDDEN_VISION_IMPORT_PREFIXES,
    )

    assert violations == {}


def test_safety_does_not_import_runtime_edges_or_desktop() -> None:
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "safety",
        FORBIDDEN_SAFETY_IMPORT_PREFIXES,
    )

    assert violations == {}


def test_desktop_uses_safety_without_runtime_edges() -> None:
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "desktop",
        FORBIDDEN_DESKTOP_IMPORT_PREFIXES,
    )

    assert violations == {}


def test_skills_do_not_import_runtime_edges_or_desktop() -> None:
    violations = forbidden_imports_under(
        PACKAGE_ROOT / "skills",
        FORBIDDEN_SKILLS_IMPORT_PREFIXES,
    )

    assert violations == {}


def forbidden_imports_under(
    module_path: Path,
    forbidden_prefixes: tuple[str, ...],
) -> dict[str, list[str]]:
    paths = sorted(module_path.rglob("*.py"))
    violations = {
        str(path): sorted(
            module
            for module in imported_modules(path)
            if module.startswith(forbidden_prefixes)
        )
        for path in paths
    }
    return {path: modules for path, modules in violations.items() if modules}
