from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from private_ai_companion import PROJECT_NAME
from private_ai_companion.avatar import AvatarExpression
from private_ai_companion.bootstrap import Application

InputReader = Callable[[str], str]

EXIT_COMMANDS = {"/exit", "/quit", "exit", "quit"}


class RichCliApp:
    def __init__(
        self,
        *,
        application: Application,
        console: Console | None = None,
        input_reader: InputReader | None = None,
    ) -> None:
        self._application = application
        self._console = console or Console()
        self._input_reader = input_reader or self._read_prompt

    async def run_interactive(self) -> int:
        self._render_startup()
        await self._application.start()
        try:
            self._console.print(
                "[dim]Digite /exit para encerrar. Esta CLI ainda usa resposta local "
                "de fundacao.[/dim]"
            )
            while True:
                try:
                    raw_text = self._input_reader("Voce")
                except (EOFError, KeyboardInterrupt):
                    self._console.print("[bold green]Encerrando.[/bold green]")
                    return 0
                if self._is_exit_command(raw_text):
                    self._console.print("[bold green]Encerrando.[/bold green]")
                    return 0
                if not raw_text.strip():
                    self._console.print(
                        "[yellow]Digite uma mensagem para conversar.[/yellow]"
                    )
                    continue

                await self._handle_turn(raw_text)
        finally:
            await self._application.stop(reason="cli_session_finished")

    async def run_single_turn(self, text: str) -> int:
        self._render_startup()
        await self._application.start()
        try:
            await self._handle_turn(text)
            return 0
        finally:
            await self._application.stop(reason="cli_single_turn_finished")

    async def run_voice_file(self, path: Path) -> int:
        self._render_startup()
        await self._application.start()
        try:
            turn = await self._application.handle_user_voice_file(path)
            if turn.text is None:
                self._console.print(
                    "[yellow]Entrada de voz ignorada: "
                    f"{turn.voice.ignored_reason or 'sem transcricao'}[/yellow]"
                )
                return 0

            self._console.print(
                "[bold blue]Voz transcrita:[/bold blue] "
                f"{turn.voice.transcript.text if turn.voice.transcript else ''}"
            )
            self._console.print(
                f"[bold magenta]{self._application.persona.display_name}:"
                f"[/bold magenta] {turn.text.assistant.text}"
            )
            return 0
        finally:
            await self._application.stop(reason="cli_voice_file_finished")

    async def run_avatar_expression(self, expression: AvatarExpression) -> int:
        self._render_startup()
        await self._application.start()
        try:
            result = await self._application.set_avatar_expression(expression)
            self._console.print(
                "[bold cyan]Avatar:[/bold cyan] "
                f"{expression.value} via {result.provider_id} ({result.status.value})"
            )
            return 0
        finally:
            await self._application.stop(reason="cli_avatar_expression_finished")

    def _render_startup(self) -> None:
        figlet = Figlet(font="small")
        self._console.print(Text(figlet.renderText(PROJECT_NAME), style="bold cyan"))
        self._console.print(
            Panel.fit(
                "private-ai-companion\n"
                "CLI inicial com Rich/Pyfiglet\n"
                "Conversa por texto local com persona configuravel",
                title="Startup",
                border_style="cyan",
            )
        )

    async def _handle_turn(self, raw_text: str) -> None:
        turn = await self._application.handle_user_text(raw_text)
        self._console.print(f"[bold blue]Voce:[/bold blue] {turn.user.text}")
        self._console.print(
            f"[bold magenta]{self._application.persona.display_name}:[/bold magenta] "
            f"{turn.assistant.text}"
        )

    def _read_prompt(self, prompt: str) -> str:
        return Prompt.ask(f"[bold blue]{prompt}[/bold blue]")

    @staticmethod
    def _is_exit_command(text: str) -> bool:
        return text.strip().casefold() in EXIT_COMMANDS
