from __future__ import annotations

import asyncio
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import cast

from private_ai_companion.adapters.avatar import VTubeStudioAvatarProvider
from private_ai_companion.avatar import (
    AvatarExpression,
    AvatarExpressionRequest,
    AvatarLipsyncFrame,
    AvatarProviderStatus,
)


def test_vtube_studio_provider_triggers_expression_hotkey() -> None:
    transport = FakeVTubeStudioTransport()
    provider = VTubeStudioAvatarProvider(
        provider_id="vtube-studio",
        host="localhost",
        port=8001,
        plugin_name="test companion",
        plugin_developer="test developer",
        expression_hotkeys={AvatarExpression.HAPPY: "hotkey-happy"},
        request_token_on_connect=True,
        transport=transport,
    )

    result = asyncio.run(
        provider.apply_expression(
            AvatarExpressionRequest(expression=AvatarExpression.HAPPY)
        )
    )

    assert result.status is AvatarProviderStatus.APPLIED
    assert [payload["messageType"] for payload in transport.payloads] == [
        "AuthenticationTokenRequest",
        "AuthenticationRequest",
        "HotkeyTriggerRequest",
    ]
    assert transport.payloads[-1]["data"] == {"hotkeyID": "hotkey-happy"}


def test_vtube_studio_provider_skips_unmapped_expression() -> None:
    transport = FakeVTubeStudioTransport()
    provider = VTubeStudioAvatarProvider(
        provider_id="vtube-studio",
        host="localhost",
        port=8001,
        plugin_name="test companion",
        plugin_developer="test developer",
        expression_hotkeys={},
        transport=transport,
    )

    result = asyncio.run(
        provider.apply_expression(
            AvatarExpressionRequest(expression=AvatarExpression.CONFUSED)
        )
    )

    assert result.status is AvatarProviderStatus.SKIPPED
    assert transport.payloads == []


def test_vtube_studio_provider_injects_lipsync_parameter() -> None:
    transport = FakeVTubeStudioTransport()
    provider = VTubeStudioAvatarProvider(
        provider_id="vtube-studio",
        host="localhost",
        port=8001,
        plugin_name="test companion",
        plugin_developer="test developer",
        expression_hotkeys={},
        authentication_token="token",
        transport=transport,
    )

    result = asyncio.run(
        provider.apply_lipsync(
            AvatarLipsyncFrame(
                mouth_open=0.4,
                parameter_name="MouthOpen",
                weight=0.5,
            )
        )
    )

    assert result.status is AvatarProviderStatus.APPLIED
    assert [payload["messageType"] for payload in transport.payloads] == [
        "AuthenticationRequest",
        "InjectParameterDataRequest",
    ]
    data = transport.payloads[-1]["data"]
    assert isinstance(data, dict)
    parameter_values = cast(object, data["parameterValues"])
    assert parameter_values == [{"id": "MouthOpen", "value": 0.4, "weight": 0.5}]


def empty_payloads() -> list[dict[str, object]]:
    return []


@dataclass(slots=True)
class FakeVTubeStudioTransport:
    payloads: list[dict[str, object]] = field(default_factory=empty_payloads)
    closed: bool = False

    async def send(self, payload: Mapping[str, object]) -> Mapping[str, object]:
        stored = dict(payload)
        self.payloads.append(stored)
        message_type = stored["messageType"]
        if message_type == "AuthenticationTokenRequest":
            return {
                "messageType": "AuthenticationTokenResponse",
                "data": {"authenticationToken": "token"},
            }
        if message_type == "AuthenticationRequest":
            return {
                "messageType": "AuthenticationResponse",
                "data": {"authenticated": True, "reason": "Token valid."},
            }
        return {
            "messageType": str(message_type).replace("Request", "Response"),
            "data": {},
        }

    async def close(self) -> None:
        self.closed = True
