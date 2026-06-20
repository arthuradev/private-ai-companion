from __future__ import annotations

from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from private_ai_companion import PROJECT_NAME
from private_ai_companion.bootstrap import Application


@dataclass(frozen=True, slots=True)
class StatusCount:
    name: str
    count: int


@dataclass(frozen=True, slots=True)
class DashboardSnapshot:
    project_name: str
    runtime_phase: str
    persona_display_name: str
    persona_language: str
    llm_provider_ids: tuple[str, ...]
    avatar_provider_id: str
    avatar_expression: str
    capture_provider_id: str
    vision_provider_id: str
    speech_pending_count: int
    memory_counts: tuple[StatusCount, ...]
    desktop_executor_id: str
    allowed_action_types: tuple[str, ...]
    confirmation_risk_levels: tuple[str, ...]
    allow_high_risk: bool
    allow_critical_risk: bool
    allowed_app_ids: tuple[str, ...]
    notes_enabled: bool
    active_window_title_enabled: bool
    audit_record_count: int
    registered_skill_ids: tuple[str, ...]
    enabled_skill_ids: tuple[str, ...]

    @property
    def pending_memory_count(self) -> int:
        return next(
            (
                item.count
                for item in self.memory_counts
                if item.name == "pending_review"
            ),
            0,
        )


def build_dashboard_snapshot(application: Application) -> DashboardSnapshot:
    desktop_policy = application.desktop_actions.action_policy
    desktop_permissions = application.desktop_actions.permission_policy
    skill_policy = application.skills.policy
    memory_counts = tuple(
        StatusCount(name=status, count=count)
        for status, count in application.memory_status_counts().items()
    )

    return DashboardSnapshot(
        project_name=PROJECT_NAME,
        runtime_phase=application.orchestrator.state.phase.value,
        persona_display_name=application.persona.display_name,
        persona_language=application.persona.primary_language,
        llm_provider_ids=application.llm_router.provider_ids,
        avatar_provider_id=application.avatar.provider_id,
        avatar_expression=application.avatar.current_expression.value,
        capture_provider_id=application.vision.capture_provider_id,
        vision_provider_id=application.vision.vision_provider_id,
        speech_pending_count=application.speech_queue.pending_count,
        memory_counts=memory_counts,
        desktop_executor_id=application.desktop_actions.executor_id,
        allowed_action_types=desktop_policy.allowed_action_types,
        confirmation_risk_levels=tuple(
            level.value for level in desktop_policy.require_confirmation_for
        ),
        allow_high_risk=desktop_policy.allow_high_risk,
        allow_critical_risk=desktop_policy.allow_critical_risk,
        allowed_app_ids=desktop_permissions.allowed_app_ids,
        notes_enabled=desktop_permissions.notes_enabled,
        active_window_title_enabled=desktop_permissions.active_window_title_enabled,
        audit_record_count=len(application.desktop_actions.audit_records),
        registered_skill_ids=application.skills.skill_ids,
        enabled_skill_ids=skill_policy.enabled_skill_ids
        if skill_policy.enabled
        else (),
    )


class RichDashboardRenderer:
    def __init__(self, console: Console | None = None) -> None:
        self._console = console or Console()

    def render(self, snapshot: DashboardSnapshot) -> None:
        self._console.print(
            Panel.fit(
                "Dashboard local para status, configuracao, memoria e permissoes.",
                title=f"{snapshot.project_name} dashboard",
                border_style="cyan",
            )
        )
        self._console.print(self._configuration_table(snapshot))
        self._console.print(self._memory_table(snapshot))
        self._console.print(self._permissions_table(snapshot))
        self._console.print(self._skills_table(snapshot))

    @staticmethod
    def _configuration_table(snapshot: DashboardSnapshot) -> Table:
        table = Table(title="Configuracao e status", show_header=True)
        table.add_column("Campo", style="bold cyan")
        table.add_column("Valor")
        table.add_row("Runtime", snapshot.runtime_phase)
        table.add_row("Persona", snapshot.persona_display_name)
        table.add_row("Idioma", snapshot.persona_language)
        table.add_row("LLM providers", _join(snapshot.llm_provider_ids))
        table.add_row("Avatar provider", snapshot.avatar_provider_id)
        table.add_row("Avatar expressao", snapshot.avatar_expression)
        table.add_row("Screen capture", snapshot.capture_provider_id)
        table.add_row("Vision provider", snapshot.vision_provider_id)
        table.add_row("Speech pendente", str(snapshot.speech_pending_count))
        return table

    @staticmethod
    def _memory_table(snapshot: DashboardSnapshot) -> Table:
        table = Table(title="Memoria local", show_header=True)
        table.add_column("Status", style="bold cyan")
        table.add_column("Quantidade", justify="right")
        for item in snapshot.memory_counts:
            table.add_row(item.name, str(item.count))
        return table

    @staticmethod
    def _permissions_table(snapshot: DashboardSnapshot) -> Table:
        table = Table(title="Permissoes e acoes locais", show_header=True)
        table.add_column("Campo", style="bold cyan")
        table.add_column("Valor")
        table.add_row("Executor", snapshot.desktop_executor_id)
        table.add_row("Acoes permitidas", _join(snapshot.allowed_action_types))
        table.add_row(
            "Confirmacao para risco", _join(snapshot.confirmation_risk_levels)
        )
        table.add_row("Alto risco habilitado", _yes_no(snapshot.allow_high_risk))
        table.add_row("Critico habilitado", _yes_no(snapshot.allow_critical_risk))
        table.add_row("Apps permitidos", _join(snapshot.allowed_app_ids))
        table.add_row("Notas locais", _yes_no(snapshot.notes_enabled))
        table.add_row(
            "Titulo janela ativa",
            _yes_no(snapshot.active_window_title_enabled),
        )
        table.add_row("Auditorias de acao", str(snapshot.audit_record_count))
        return table

    @staticmethod
    def _skills_table(snapshot: DashboardSnapshot) -> Table:
        table = Table(title="Skills", show_header=True)
        table.add_column("Campo", style="bold cyan")
        table.add_column("Valor")
        table.add_row("Registradas", _join(snapshot.registered_skill_ids))
        table.add_row("Habilitadas", _join(snapshot.enabled_skill_ids))
        return table


class RichDashboardApp:
    def __init__(
        self,
        *,
        application: Application,
        console: Console | None = None,
    ) -> None:
        self._application = application
        self._renderer = RichDashboardRenderer(console)

    async def run_once(self) -> int:
        await self._application.start()
        try:
            self._renderer.render(build_dashboard_snapshot(self._application))
            return 0
        finally:
            await self._application.stop(reason="dashboard_finished")


def _join(values: tuple[str, ...]) -> str:
    return ", ".join(values) if values else "nenhum"


def _yes_no(value: bool) -> str:
    return "sim" if value else "nao"
