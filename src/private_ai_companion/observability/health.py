from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from private_ai_companion.observability.models import (
    HealthCheckResult,
    HealthReport,
    HealthStatus,
    JsonScalar,
)

HealthCheck = Callable[[], HealthCheckResult]


def _empty_details() -> dict[str, JsonScalar]:
    return {}


@dataclass(frozen=True, slots=True)
class ComponentHealthCheck:
    component_id: str
    check: HealthCheck


@dataclass(frozen=True, slots=True)
class HealthCheckService:
    checks: tuple[ComponentHealthCheck, ...]
    enabled: bool = True

    def run(self) -> HealthReport:
        if not self.enabled:
            return HealthReport(
                status=HealthStatus.WARN,
                checks=(
                    HealthCheckResult(
                        component_id="observability.health",
                        status=HealthStatus.WARN,
                        message="health_checks_disabled",
                    ),
                ),
            )

        results = tuple(self._run_check(check) for check in self.checks)
        return HealthReport(status=_overall_status(results), checks=results)

    @staticmethod
    def _run_check(check: ComponentHealthCheck) -> HealthCheckResult:
        try:
            return check.check()
        except Exception as error:
            return HealthCheckResult(
                component_id=check.component_id,
                status=HealthStatus.FAIL,
                message="health_check_failed",
                details={"error_type": type(error).__name__},
            )


def pass_check(
    component_id: str,
    message: str,
    *,
    details: dict[str, JsonScalar] | None = None,
) -> HealthCheckResult:
    return HealthCheckResult(
        component_id=component_id,
        status=HealthStatus.PASS,
        message=message,
        details=details or _empty_details(),
    )


def warn_check(
    component_id: str,
    message: str,
    *,
    details: dict[str, JsonScalar] | None = None,
) -> HealthCheckResult:
    return HealthCheckResult(
        component_id=component_id,
        status=HealthStatus.WARN,
        message=message,
        details=details or _empty_details(),
    )


def fail_check(
    component_id: str,
    message: str,
    *,
    details: dict[str, JsonScalar] | None = None,
) -> HealthCheckResult:
    return HealthCheckResult(
        component_id=component_id,
        status=HealthStatus.FAIL,
        message=message,
        details=details or _empty_details(),
    )


def _overall_status(results: tuple[HealthCheckResult, ...]) -> HealthStatus:
    if any(result.status is HealthStatus.FAIL for result in results):
        return HealthStatus.FAIL
    if any(result.status is HealthStatus.WARN for result in results):
        return HealthStatus.WARN
    return HealthStatus.PASS
