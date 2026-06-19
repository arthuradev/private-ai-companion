from __future__ import annotations

import asyncio
from dataclasses import fields
from pathlib import Path

from private_ai_companion.adapters.desktop import SafeLocalDesktopExecutor
from private_ai_companion.core import BaseEvent, EventBus
from private_ai_companion.desktop import (
    DesktopActionRequest,
    DesktopActionService,
    DesktopActionType,
    DesktopPermissionPolicy,
)
from private_ai_companion.safety import (
    ActionExecutionStatus,
    ActionPolicy,
    InMemoryActionAuditLog,
    RiskClassifier,
)


def build_security_service(
    tmp_path: Path,
    events: list[BaseEvent] | None = None,
) -> DesktopActionService:
    event_bus = EventBus()
    if events is not None:
        event_bus.subscribe(BaseEvent, events.append)
    return DesktopActionService(
        event_bus=event_bus,
        executor=SafeLocalDesktopExecutor(
            notes_directory=tmp_path,
            allowed_apps={"calculator": "Calculator"},
        ),
        risk_classifier=RiskClassifier(),
        action_policy=ActionPolicy(
            allowed_action_types=(
                DesktopActionType.CREATE_NOTE.value,
                DesktopActionType.OPEN_ALLOWED_APP.value,
            )
        ),
        permission_policy=DesktopPermissionPolicy(
            allowed_action_types=(
                DesktopActionType.CREATE_NOTE.value,
                DesktopActionType.OPEN_ALLOWED_APP.value,
            ),
            allowed_app_ids=("calculator",),
        ),
        audit_log=InMemoryActionAuditLog(),
    )


def test_critical_shell_action_is_denied_even_when_confirmed(tmp_path: Path) -> None:
    service = build_security_service(tmp_path)

    result = asyncio.run(
        service.perform(
            DesktopActionRequest(
                action_type="system.run_shell",
                parameters={"command": "echo unsafe"},
                user_confirmed=True,
            )
        )
    )

    assert result.status is ActionExecutionStatus.DENIED
    assert result.risk.value == "critical"
    assert result.message == "critical_actions_prohibited"


def test_medium_action_requires_confirmation_by_default(tmp_path: Path) -> None:
    service = build_security_service(tmp_path)

    result = asyncio.run(
        service.perform(
            DesktopActionRequest(
                action_type=DesktopActionType.CREATE_NOTE.value,
                parameters={"title": "Private", "body": "do not audit body"},
            )
        )
    )

    assert result.status is ActionExecutionStatus.REQUIRES_CONFIRMATION
    assert not list(tmp_path.glob("*.md"))


def test_audit_records_do_not_store_action_parameters(tmp_path: Path) -> None:
    service = build_security_service(tmp_path)

    result = asyncio.run(
        service.perform(
            DesktopActionRequest(
                action_type=DesktopActionType.CREATE_NOTE.value,
                parameters={"title": "Secret", "body": "token=abc123"},
            )
        )
    )

    assert result.audit_record is not None
    field_names = {field.name for field in fields(type(result.audit_record))}
    assert "parameters" not in field_names
    assert "body" not in field_names


def test_desktop_events_do_not_include_action_parameters(tmp_path: Path) -> None:
    events: list[BaseEvent] = []
    service = build_security_service(tmp_path, events)

    asyncio.run(
        service.perform(
            DesktopActionRequest(
                action_type=DesktopActionType.CREATE_NOTE.value,
                parameters={"title": "Secret", "body": "token=abc123"},
                dry_run_only=True,
            )
        )
    )

    event_field_names = {
        field.name for event in events for field in fields(type(event))
    }
    assert "parameters" not in event_field_names
    assert "body" not in event_field_names
    assert "command" not in event_field_names
