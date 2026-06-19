from __future__ import annotations

import json
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from importlib import import_module
from typing import Protocol, cast
from uuid import uuid4

from private_ai_companion.avatar import (
    AvatarExpression,
    AvatarExpressionRequest,
    AvatarLipsyncFrame,
    AvatarProviderError,
    AvatarProviderResult,
    AvatarProviderStatus,
)

VTS_API_NAME = "VTubeStudioPublicAPI"
VTS_API_VERSION = "1.0"


class VTubeStudioTransport(Protocol):
    async def send(self, payload: Mapping[str, object]) -> Mapping[str, object]:
        """Send one VTube Studio API payload and return its response."""
        ...

    async def close(self) -> None:
        """Close the transport."""
        ...


class _WebSocketConnection(Protocol):
    async def send(self, message: str) -> None:
        """Send a websocket text message."""
        ...

    async def recv(self) -> str:
        """Receive a websocket text message."""
        ...

    async def close(self) -> None:
        """Close the websocket."""
        ...


@dataclass(slots=True)
class WebSocketVTubeStudioTransport:
    connection: _WebSocketConnection

    @classmethod
    async def connect(cls, url: str) -> WebSocketVTubeStudioTransport:
        try:
            module = import_module("websockets")
        except ModuleNotFoundError as exc:
            raise AvatarProviderError(
                "websockets is not installed. Install the optional avatar extra "
                "before selecting provider_id='vtube-studio'."
            ) from exc

        connector = cast(
            Callable[[str], Awaitable[_WebSocketConnection]],
            module.__dict__["connect"],
        )
        return cls(connection=await connector(url))

    async def send(self, payload: Mapping[str, object]) -> Mapping[str, object]:
        await self.connection.send(json.dumps(dict(payload)))
        raw_response = await self.connection.recv()
        response = json.loads(raw_response)
        if not isinstance(response, Mapping):
            raise AvatarProviderError("VTube Studio returned a non-object response")
        return cast(Mapping[str, object], response)

    async def close(self) -> None:
        await self.connection.close()


@dataclass(slots=True)
class VTubeStudioAvatarProvider:
    provider_id: str
    host: str
    port: int
    plugin_name: str
    plugin_developer: str
    expression_hotkeys: Mapping[AvatarExpression, str]
    authentication_token: str | None = None
    request_token_on_connect: bool = False
    transport: VTubeStudioTransport | None = None

    @property
    def websocket_url(self) -> str:
        return f"ws://{self.host}:{self.port}"

    async def connect(self) -> None:
        if self.transport is None:
            self.transport = await WebSocketVTubeStudioTransport.connect(
                self.websocket_url
            )

        if self.authentication_token is None and self.request_token_on_connect:
            self.authentication_token = await self._request_authentication_token()

        if self.authentication_token is not None:
            await self._authenticate(self.authentication_token)

    async def disconnect(self) -> None:
        if self.transport is not None:
            await self.transport.close()
            self.transport = None

    async def apply_expression(
        self,
        request: AvatarExpressionRequest,
    ) -> AvatarProviderResult:
        hotkey_id = self.expression_hotkeys.get(request.expression)
        if not hotkey_id:
            return AvatarProviderResult(
                provider_id=self.provider_id,
                status=AvatarProviderStatus.SKIPPED,
                expression=request.expression,
                detail=f"no_hotkey_configured_for_{request.expression.value}",
                request_id=request.request_id,
            )

        await self.connect()
        await self._send_request(
            "HotkeyTriggerRequest",
            {"hotkeyID": hotkey_id},
        )
        return AvatarProviderResult(
            provider_id=self.provider_id,
            status=AvatarProviderStatus.APPLIED,
            expression=request.expression,
            detail="vtube_studio_hotkey_triggered",
            request_id=request.request_id,
        )

    async def apply_lipsync(
        self,
        frame: AvatarLipsyncFrame,
    ) -> AvatarProviderResult:
        await self.connect()
        await self._send_request(
            "InjectParameterDataRequest",
            {
                "faceFound": True,
                "mode": "set",
                "parameterValues": [
                    {
                        "id": frame.parameter_name,
                        "value": frame.mouth_open,
                        "weight": frame.weight,
                    }
                ],
            },
        )
        return AvatarProviderResult(
            provider_id=self.provider_id,
            status=AvatarProviderStatus.APPLIED,
            detail="vtube_studio_lipsync_parameter_injected",
            request_id=frame.request_id,
        )

    async def _request_authentication_token(self) -> str:
        data = await self._send_request(
            "AuthenticationTokenRequest",
            {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.plugin_developer,
            },
        )
        token = data.get("authenticationToken")
        if not isinstance(token, str) or not token:
            raise AvatarProviderError("VTube Studio did not return an auth token")
        return token

    async def _authenticate(self, token: str) -> None:
        data = await self._send_request(
            "AuthenticationRequest",
            {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.plugin_developer,
                "authenticationToken": token,
            },
        )
        if data.get("authenticated") is not True:
            reason = data.get("reason")
            raise AvatarProviderError(
                f"VTube Studio authentication failed: {reason or 'unknown reason'}"
            )

    async def _send_request(
        self,
        message_type: str,
        data: Mapping[str, object] | None = None,
    ) -> Mapping[str, object]:
        if self.transport is None:
            raise AvatarProviderError("VTube Studio transport is not connected")

        payload: dict[str, object] = {
            "apiName": VTS_API_NAME,
            "apiVersion": VTS_API_VERSION,
            "requestID": f"pac-{uuid4().hex[:32]}",
            "messageType": message_type,
            "data": dict(data or {}),
        }
        response = await self.transport.send(payload)
        if response.get("messageType") == "APIError":
            error_data = response.get("data")
            if isinstance(error_data, Mapping):
                error_mapping = cast(Mapping[str, object], error_data)
                message = error_mapping.get("message")
                raise AvatarProviderError(str(message or "VTube Studio API error"))
            raise AvatarProviderError("VTube Studio API error")

        response_data = response.get("data", {})
        if not isinstance(response_data, Mapping):
            raise AvatarProviderError("VTube Studio returned invalid data")
        return cast(Mapping[str, object], response_data)
