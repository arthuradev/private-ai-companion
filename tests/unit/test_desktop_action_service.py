from __future__ import annotations

import asyncio
from pathlib import Path

from private_ai_companion.adapters.desktop import SafeLocalDesktopExecutor
from private_ai_companion.core import (
    ActionExecuted,
    ActionIntentCreated,
    AuditEventCreated,
    BaseEvent,
    EventBus,
    PermissionRequired,
)
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


def build_service(
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
                DesktopActionType.READ_ACTIVE_WINDOW_TITLE.value,
                DesktopActionType.CREATE_NOTE.value,
                DesktopActionType.OPEN_ALLOWED_APP.value,
            )
        ),
        permission_policy=DesktopPermissionPolicy(
            allowed_action_types=(
                DesktopActionType.READ_ACTIVE_WINDOW_TITLE.value,
                DesktopActionType.CREATE_NOTE.value,
                DesktopActionType.OPEN_ALLOWED_APP.value,
            ),
            allowed_app_ids=("calculator",),
        ),
        audit_log=InMemoryActionAuditLog(),
    )


def test_desktop_action_service_requires_confirmation_before_execution(
    tmp_path: Path,
) -> None:
    service = build_service(tmp_path)

    result = asyncio.run(
        service.perform(
            DesktopActionRequest(
                action_type=DesktopActionType.CREATE_NOTE.value,
                parameters={"title": "Needs confirmation", "body": "not yet"},
            )
        )
    )

    assert result.status is ActionExecutionStatus.REQUIRES_CONFIRMATION
    assert result.dry_run is not None
    assert not list(tmp_path.glob("*.md"))
    assert len(service.audit_records) == 1


def test_desktop_action_service_executes_confirmed_note(tmp_path: Path) -> None:
    service = build_service(tmp_path)

    result = asyncio.run(
        service.perform(
            DesktopActionRequest(
                action_type=DesktopActionType.CREATE_NOTE.value,
                parameters={"title": "Confirmed", "body": "write it"},
                user_confirmed=True,
            )
        )
    )

    assert result.status is ActionExecutionStatus.EXECUTED
    assert Path(result.output["note_path"]).is_file()
    assert len(service.audit_records) == 1


def test_desktop_action_service_dry_run_does_not_execute(tmp_path: Path) -> None:
    service = build_service(tmp_path)

    result = asyncio.run(
        service.perform(
            DesktopActionRequest(
                action_type=DesktopActionType.CREATE_NOTE.value,
                parameters={"title": "Dry run", "body": "not written"},
                dry_run_only=True,
            )
        )
    )

    assert result.status is ActionExecutionStatus.DRY_RUN
    assert not list(tmp_path.glob("*.md"))


def test_desktop_action_service_blocks_unallowlisted_app(tmp_path: Path) -> None:
    service = build_service(tmp_path)

    result = asyncio.run(
        service.perform(
            DesktopActionRequest(
                action_type=DesktopActionType.OPEN_ALLOWED_APP.value,
                parameters={"app_id": "browser"},
                user_confirmed=True,
            )
        )
    )

    assert result.status is ActionExecutionStatus.DENIED
    assert result.message == "app_not_allowlisted"


def test_desktop_action_service_publishes_safe_events(tmp_path: Path) -> None:
    events: list[BaseEvent] = []
    service = build_service(tmp_path, events)

    result = asyncio.run(
        service.perform(
            DesktopActionRequest(
                action_type=DesktopActionType.READ_ACTIVE_WINDOW_TITLE.value,
                user_confirmed=True,
            )
        )
    )

    assert result.status is ActionExecutionStatus.EXECUTED
    assert [type(event) for event in events] == [
        ActionIntentCreated,
        ActionExecuted,
        AuditEventCreated,
    ]
    assert all(not hasattr(event, "parameters") for event in events)


def test_desktop_action_service_publishes_permission_required_event(
    tmp_path: Path,
) -> None:
    events: list[BaseEvent] = []
    service = build_service(tmp_path, events)

    result = asyncio.run(
        service.perform(
            DesktopActionRequest(
                action_type=DesktopActionType.READ_ACTIVE_WINDOW_TITLE.value,
            )
        )
    )

    assert result.status is ActionExecutionStatus.REQUIRES_CONFIRMATION
    assert [type(event) for event in events] == [
        ActionIntentCreated,
        PermissionRequired,
        AuditEventCreated,
    ]
