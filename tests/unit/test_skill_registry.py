from __future__ import annotations

import pytest

from private_ai_companion.skills import (
    SkillManifest,
    SkillManifestError,
    SkillRegistry,
    SkillRegistryError,
    StatusSkill,
    validate_manifest,
)


def test_validate_manifest_accepts_status_skill() -> None:
    validate_manifest(StatusSkill().manifest)


def test_validate_manifest_rejects_bad_version() -> None:
    with pytest.raises(SkillManifestError, match="invalid skill version"):
        validate_manifest(
            SkillManifest(
                skill_id="builtin.bad",
                name="Bad",
                description="Bad version",
                version="v1",
            )
        )


def test_skill_registry_registers_and_lists_manifests() -> None:
    registry = SkillRegistry()
    registry.register(StatusSkill())

    assert registry.get("builtin.status").manifest.name == "Status"
    assert [manifest.skill_id for manifest in registry.list_manifests()] == [
        "builtin.status"
    ]


def test_skill_registry_rejects_duplicate_skill() -> None:
    registry = SkillRegistry()
    registry.register(StatusSkill())

    with pytest.raises(SkillRegistryError, match="already registered"):
        registry.register(StatusSkill())
