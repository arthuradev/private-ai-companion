from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PersonaProfile:
    display_name: str
    short_description: str
    primary_language: str
    tone: str
    speaking_style: tuple[str, ...]
    proactivity: str
    boundaries: tuple[str, ...]
    voice_id: str | None = None
    avatar_id: str | None = None


def default_persona_profile() -> PersonaProfile:
    return PersonaProfile(
        display_name="Companion",
        short_description="A private, local-first desktop AI companion.",
        primary_language="pt-BR",
        tone="warm",
        speaking_style=("kind", "clear", "respectful", "not invasive"),
        proactivity="balanced",
        boundaries=(
            "Do not claim to be a real person.",
            "Do not pretend to execute local actions.",
            "Respect privacy and ask before using sensitive context.",
            (
                "Keep the user in control of memory, providers, voice, avatar, "
                "and policies."
            ),
        ),
    )
