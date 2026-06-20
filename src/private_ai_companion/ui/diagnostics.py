from __future__ import annotations

from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from private_ai_companion.bootstrap import Application
from private_ai_companion.observability import DiagnosticsSnapshot


@dataclass(frozen=True, slots=True)
class RichDiagnosticsRenderer:
    console: Console

    def render(self, snapshot: DiagnosticsSnapshot) -> None:
        self.console.print(
            Panel.fit(
                f"Health: {snapshot.health.status.value} | "
                f"Eventos: {snapshot.metrics.total_events} | "
                f"Logs: {len(snapshot.log_records)} | "
                f"Replay: {len(snapshot.replay_records)}",
                title="Diagnostico local",
                border_style="cyan",
            )
        )
        self.console.print(self._health_table(snapshot))
        self.console.print(self._metrics_table(snapshot))
        self.console.print(self._replay_table(snapshot))
        self.console.print(self._logs_table(snapshot))

    @staticmethod
    def _health_table(snapshot: DiagnosticsSnapshot) -> Table:
        table = Table(title="Health checks", show_header=True)
        table.add_column("Componente", style="bold cyan")
        table.add_column("Status")
        table.add_column("Mensagem")
        for check in snapshot.health.checks:
            table.add_row(check.component_id, check.status.value, check.message)
        return table

    @staticmethod
    def _metrics_table(snapshot: DiagnosticsSnapshot) -> Table:
        table = Table(title="Metricas de eventos", show_header=True)
        table.add_column("Evento", style="bold cyan")
        table.add_column("Quantidade", justify="right")
        for event_name, count in sorted(snapshot.metrics.events_by_name.items()):
            table.add_row(event_name, str(count))
        if not snapshot.metrics.events_by_name:
            table.add_row("nenhum", "0")
        return table

    @staticmethod
    def _replay_table(snapshot: DiagnosticsSnapshot) -> Table:
        table = Table(title="Replay sanitizado", show_header=True)
        table.add_column("Evento", style="bold cyan")
        table.add_column("Source")
        table.add_column("Sensibilidade")
        table.add_column("Campos")
        table.add_column("Redigidos")
        for record in snapshot.replay_records[-10:]:
            table.add_row(
                record.event_name,
                record.source,
                record.sensitivity,
                str(len(record.fields)),
                str(len(record.redacted_fields)),
            )
        if not snapshot.replay_records:
            table.add_row("nenhum", "-", "-", "0", "0")
        return table

    @staticmethod
    def _logs_table(snapshot: DiagnosticsSnapshot) -> Table:
        table = Table(title="Logs estruturados", show_header=True)
        table.add_column("Nivel", style="bold cyan")
        table.add_column("Evento")
        table.add_column("Mensagem")
        table.add_column("Redigidos")
        for record in snapshot.log_records[-10:]:
            table.add_row(
                record.level.value,
                record.event_name,
                record.message,
                str(len(record.redacted_fields)),
            )
        if not snapshot.log_records:
            table.add_row("nenhum", "-", "-", "0")
        return table


class RichDiagnosticsApp:
    def __init__(
        self,
        *,
        application: Application,
        console: Console | None = None,
    ) -> None:
        self._application = application
        self._renderer = RichDiagnosticsRenderer(console or Console())

    async def run_once(self) -> int:
        await self._application.start()
        try:
            self._renderer.render(self._application.diagnostics_snapshot())
            return 0
        finally:
            await self._application.stop(reason="diagnostics_finished")
