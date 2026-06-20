from __future__ import annotations

from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from private_ai_companion.bootstrap import Application
from private_ai_companion.ui.dashboard import (
    DashboardSnapshot,
    build_dashboard_snapshot,
)


@dataclass(frozen=True, slots=True)
class TrayMenuItem:
    label: str
    command: str
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class TraySnapshot:
    status: str
    tooltip: str
    menu_items: tuple[TrayMenuItem, ...]


def build_tray_snapshot(dashboard: DashboardSnapshot) -> TraySnapshot:
    pending = dashboard.pending_memory_count
    memory_label = f"Revisar memoria ({pending} pendente)"
    return TraySnapshot(
        status=dashboard.runtime_phase,
        tooltip=(
            f"{dashboard.project_name} | {dashboard.persona_display_name} | "
            f"runtime={dashboard.runtime_phase}"
        ),
        menu_items=(
            TrayMenuItem(label="Abrir dashboard", command="dashboard"),
            TrayMenuItem(label="Iniciar conversa", command="chat"),
            TrayMenuItem(
                label=memory_label,
                command="memory-review",
                enabled=pending > 0,
            ),
            TrayMenuItem(label="Ver permissoes", command="permissions"),
            TrayMenuItem(label="Encerrar", command="quit"),
        ),
    )


class RichTrayStatusRenderer:
    def __init__(self, console: Console | None = None) -> None:
        self._console = console or Console()

    def render(self, snapshot: TraySnapshot) -> None:
        self._console.print(
            Panel.fit(
                snapshot.tooltip,
                title="Tray status",
                border_style="cyan",
            )
        )
        table = Table(title="Tray menu", show_header=True)
        table.add_column("Item", style="bold cyan")
        table.add_column("Comando")
        table.add_column("Estado")
        for item in snapshot.menu_items:
            table.add_row(
                item.label,
                item.command,
                "habilitado" if item.enabled else "desabilitado",
            )
        self._console.print(table)


class RichTrayStatusApp:
    def __init__(
        self,
        *,
        application: Application,
        console: Console | None = None,
    ) -> None:
        self._application = application
        self._renderer = RichTrayStatusRenderer(console)

    async def run_once(self) -> int:
        await self._application.start()
        try:
            dashboard = build_dashboard_snapshot(self._application)
            self._renderer.render(build_tray_snapshot(dashboard))
            return 0
        finally:
            await self._application.stop(reason="tray_status_finished")
