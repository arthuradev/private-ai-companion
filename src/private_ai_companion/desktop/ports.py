from __future__ import annotations

from typing import Protocol

from private_ai_companion.desktop.models import (
    DesktopActionDryRun,
    DesktopActionExecutionResult,
)
from private_ai_companion.safety import ActionIntent, RiskLevel


class DesktopActionExecutor(Protocol):
    @property
    def executor_id(self) -> str:
        """Stable desktop executor id."""
        ...

    async def dry_run(
        self,
        intent: ActionIntent,
        risk: RiskLevel,
    ) -> DesktopActionDryRun:
        """Describe what would happen without performing side effects."""
        ...

    async def execute(
        self,
        intent: ActionIntent,
        risk: RiskLevel,
    ) -> DesktopActionExecutionResult:
        """Execute a previously allowed desktop action."""
        ...
