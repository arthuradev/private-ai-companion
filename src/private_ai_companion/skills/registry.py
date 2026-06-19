from __future__ import annotations

from dataclasses import dataclass, field

from private_ai_companion.skills.errors import SkillRegistryError
from private_ai_companion.skills.manifest import validate_manifest
from private_ai_companion.skills.models import SkillManifest
from private_ai_companion.skills.ports import BaseSkill


def _empty_skills() -> dict[str, BaseSkill]:
    return {}


@dataclass(slots=True)
class SkillRegistry:
    _skills: dict[str, BaseSkill] = field(default_factory=_empty_skills)

    def register(self, skill: BaseSkill) -> None:
        validate_manifest(skill.manifest)
        skill_id = skill.manifest.skill_id
        if skill_id in self._skills:
            raise SkillRegistryError(f"skill {skill_id!r} is already registered")
        self._skills[skill_id] = skill

    def get(self, skill_id: str) -> BaseSkill:
        try:
            return self._skills[skill_id]
        except KeyError as error:
            raise SkillRegistryError(f"unknown skill {skill_id!r}") from error

    def list_manifests(self) -> tuple[SkillManifest, ...]:
        return tuple(skill.manifest for skill in self._skills.values())
