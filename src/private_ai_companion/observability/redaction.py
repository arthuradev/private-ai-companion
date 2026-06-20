from __future__ import annotations

from dataclasses import fields, is_dataclass
from datetime import datetime
from enum import StrEnum

from private_ai_companion.core import BaseEvent, EventSensitivity
from private_ai_companion.observability.models import JsonScalar, SanitizedEventPayload

ALWAYS_REDACTED_FIELDS = {
    "body",
    "content",
    "parameters",
    "prompt",
    "purpose",
    "summary",
    "text",
    "title",
    "visible_text",
    "voice_id",
}

SAFE_PRIVATE_FIELDS = {
    "action_id",
    "action_type",
    "audit_id",
    "capture_provider_id",
    "cleared_items",
    "context_id",
    "decision",
    "dry_run",
    "duration_seconds",
    "effect_count",
    "executor_id",
    "expression",
    "finding_count",
    "height",
    "image_format",
    "intensity",
    "interrupted_item_id",
    "item_id",
    "label_count",
    "mode",
    "outcome",
    "persisted",
    "provider_id",
    "reason",
    "redacted",
    "request_id",
    "risk",
    "screenshot_id",
    "skill_id",
    "source",
    "status",
    "transcript_id",
    "value",
    "vision_provider_id",
    "width",
}


def sanitize_event(event: BaseEvent) -> SanitizedEventPayload:
    if not is_dataclass(event):
        return SanitizedEventPayload()

    raw_fields: dict[str, JsonScalar] = {}
    redacted_fields: list[str] = []
    sensitivity = event.metadata.sensitivity

    for item in fields(event):
        if item.name == "metadata":
            continue

        value = getattr(event, item.name)
        if _should_redact(item.name, sensitivity):
            redacted_fields.append(item.name)
            continue

        scalar = _to_json_scalar(value)
        if scalar is None and value is not None:
            redacted_fields.append(item.name)
            continue
        raw_fields[item.name] = scalar

    return SanitizedEventPayload(
        fields=raw_fields,
        redacted_fields=tuple(sorted(redacted_fields)),
    )


def _should_redact(field_name: str, sensitivity: EventSensitivity) -> bool:
    if field_name in ALWAYS_REDACTED_FIELDS:
        return True
    if sensitivity in {EventSensitivity.PRIVATE, EventSensitivity.SENSITIVE}:
        return field_name not in SAFE_PRIVATE_FIELDS
    return False


def _to_json_scalar(value: object) -> JsonScalar:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    return None
