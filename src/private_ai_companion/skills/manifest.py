from __future__ import annotations

import re

from private_ai_companion.skills.errors import SkillManifestError
from private_ai_companion.skills.models import SkillManifest

SKILL_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_.-]{2,63}$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def validate_manifest(manifest: SkillManifest) -> None:
    if not SKILL_ID_PATTERN.fullmatch(manifest.skill_id):
        raise SkillManifestError(f"invalid skill id {manifest.skill_id!r}")
    if not manifest.name.strip():
        raise SkillManifestError("skill name must be text")
    if not manifest.description.strip():
        raise SkillManifestError("skill description must be text")
    if not VERSION_PATTERN.fullmatch(manifest.version):
        raise SkillManifestError(f"invalid skill version {manifest.version!r}")
    if len(set(manifest.permissions)) != len(manifest.permissions):
        raise SkillManifestError("skill permissions must be unique")
    if len(set(manifest.allowed_action_types)) != len(manifest.allowed_action_types):
        raise SkillManifestError("skill allowed action types must be unique")
