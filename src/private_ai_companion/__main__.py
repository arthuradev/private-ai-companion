from __future__ import annotations

import asyncio
from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from pathlib import Path

from private_ai_companion import PROJECT_NAME, __version__
from private_ai_companion.avatar import AvatarExpression
from private_ai_companion.bootstrap import ApplicationConfigPaths, create_application
from private_ai_companion.ui import RichCliApp

DESKTOP_ACTION_CLI_MAP = {
    "read-active-window-title": "desktop.read_active_window_title",
    "create-note": "desktop.create_note",
    "open-allowed-app": "desktop.open_allowed_app",
}


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=PROJECT_NAME,
        description="Private local-first desktop AI companion.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="show the installed package version and exit",
    )
    parser.add_argument(
        "--once",
        metavar="TEXT",
        help="send one text message through the CLI and exit",
    )
    parser.add_argument(
        "--voice-file",
        type=Path,
        help="transcribe one explicit audio file and send it as one user message",
    )
    parser.add_argument(
        "--persona-config",
        type=Path,
        help="path to a persona TOML config file",
    )
    parser.add_argument(
        "--providers-config",
        type=Path,
        help="path to a providers TOML config file",
    )
    parser.add_argument(
        "--memory-config",
        type=Path,
        help="path to a memory TOML config file",
    )
    parser.add_argument(
        "--observability-config",
        type=Path,
        help="path to an observability TOML config file",
    )
    parser.add_argument(
        "--speech-config",
        type=Path,
        help="path to a speech TOML config file",
    )
    parser.add_argument(
        "--avatar-config",
        type=Path,
        help="path to an avatar TOML config file",
    )
    parser.add_argument(
        "--privacy-config",
        type=Path,
        help="path to a privacy TOML config file",
    )
    parser.add_argument(
        "--desktop-config",
        type=Path,
        help="path to a desktop actions TOML config file",
    )
    parser.add_argument(
        "--skills-config",
        type=Path,
        help="path to a skills TOML config file",
    )
    parser.add_argument(
        "--avatar-expression",
        choices=[expression.value for expression in AvatarExpression],
        help="apply one avatar expression and exit",
    )
    parser.add_argument(
        "--screen-context",
        action="store_true",
        help="capture one authorized temporary screen context and exit",
    )
    parser.add_argument(
        "--screen-purpose",
        default="manual_cli_screen_context",
        help="short purpose attached to an explicit screen context request",
    )
    parser.add_argument(
        "--desktop-action",
        choices=sorted(DESKTOP_ACTION_CLI_MAP),
        help="run one safe desktop action through policy and exit",
    )
    parser.add_argument(
        "--desktop-confirm",
        action="store_true",
        help="confirm one policy-gated desktop action",
    )
    parser.add_argument(
        "--desktop-dry-run",
        action="store_true",
        help="show the desktop action dry-run without executing it",
    )
    parser.add_argument(
        "--note-title",
        help="title for --desktop-action create-note",
    )
    parser.add_argument(
        "--note-body",
        default="",
        help="body for --desktop-action create-note",
    )
    parser.add_argument(
        "--app-id",
        help="allowlisted app id for --desktop-action open-allowed-app",
    )
    parser.add_argument(
        "--skill",
        help="run one enabled skill by id and exit",
    )
    parser.add_argument(
        "--skill-input",
        action="append",
        metavar="KEY=VALUE",
        help="input pair for --skill; may be passed more than once",
    )
    parser.add_argument(
        "--skill-confirm",
        action="store_true",
        help="confirm one policy-gated skill effect",
    )
    parser.add_argument(
        "--skill-dry-run",
        action="store_true",
        help="run one skill effect in dry-run mode",
    )
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="show the local dashboard and exit",
    )
    parser.add_argument(
        "--tray-status",
        action="store_true",
        help="show the local tray status model and exit",
    )
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        help="show local health checks, metrics and sanitized event replay",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    options = parser.parse_args(argv)

    if bool(options.version):
        print(f"{PROJECT_NAME} {__version__}")
        return 0

    single_action_count = sum(
        (
            options.once is not None,
            options.voice_file is not None,
            options.avatar_expression is not None,
            bool(options.screen_context),
            options.desktop_action is not None,
            options.skill is not None,
            bool(options.dashboard),
            bool(options.tray_status),
            bool(options.diagnostics),
        )
    )
    if single_action_count > 1:
        parser.error(
            "--once, --voice-file, --avatar-expression, --screen-context, "
            "--desktop-action, --skill, --dashboard, --tray-status and "
            "--diagnostics are exclusive"
        )

    if options.desktop_action == "create-note" and not options.note_title:
        parser.error("--desktop-action create-note requires --note-title")
    if options.desktop_action == "open-allowed-app" and not options.app_id:
        parser.error("--desktop-action open-allowed-app requires --app-id")
    try:
        skill_input = (
            _parse_key_value_options(options.skill_input)
            if options.skill is not None
            else {}
        )
    except ValueError as error:
        parser.error(str(error))

    cli = RichCliApp(
        application=create_application(
            config_paths=ApplicationConfigPaths(
                persona=options.persona_config,
                providers=options.providers_config,
                memory=options.memory_config,
                observability=options.observability_config,
                speech=options.speech_config,
                avatar=options.avatar_config,
                privacy=options.privacy_config,
                desktop=options.desktop_config,
                skills=options.skills_config,
            ),
        )
    )
    return _run_cli_action(cli, options, skill_input)


def _run_cli_action(
    cli: RichCliApp,
    options: Namespace,
    skill_input: dict[str, str],
) -> int:
    if _has_interaction_action(options):
        return _run_interaction_action(cli, options)
    if options.desktop_action is not None or options.skill is not None:
        return _run_tool_action(cli, options, skill_input)
    if options.dashboard or options.tray_status or options.diagnostics:
        return _run_local_ui_action(cli, options)

    return asyncio.run(cli.run_interactive())


def _has_interaction_action(options: Namespace) -> bool:
    return (
        options.once is not None
        or options.voice_file is not None
        or options.avatar_expression is not None
        or bool(options.screen_context)
    )


def _run_interaction_action(cli: RichCliApp, options: Namespace) -> int:
    if options.once is not None:
        return asyncio.run(cli.run_single_turn(str(options.once)))
    if options.voice_file is not None:
        return asyncio.run(cli.run_voice_file(Path(options.voice_file)))
    if options.avatar_expression is not None:
        return asyncio.run(
            cli.run_avatar_expression(AvatarExpression(str(options.avatar_expression)))
        )
    if options.screen_context:
        return asyncio.run(cli.run_screen_context(str(options.screen_purpose)))
    raise ValueError("expected interaction option")


def _run_tool_action(
    cli: RichCliApp,
    options: Namespace,
    skill_input: dict[str, str],
) -> int:
    if options.desktop_action is not None:
        parameters: dict[str, str] = {}
        if options.desktop_action == "create-note":
            parameters = {
                "title": str(options.note_title),
                "body": str(options.note_body),
            }
        elif options.desktop_action == "open-allowed-app":
            parameters = {"app_id": str(options.app_id)}
        return asyncio.run(
            cli.run_desktop_action(
                action_type=DESKTOP_ACTION_CLI_MAP[str(options.desktop_action)],
                parameters=parameters,
                user_confirmed=bool(options.desktop_confirm),
                dry_run_only=bool(options.desktop_dry_run),
            )
        )
    if options.skill is not None:
        return asyncio.run(
            cli.run_skill(
                skill_id=str(options.skill),
                skill_input=skill_input,
                user_confirmed=bool(options.skill_confirm),
                dry_run_only=bool(options.skill_dry_run),
            )
        )
    raise ValueError("expected desktop action or skill option")


def _run_local_ui_action(cli: RichCliApp, options: Namespace) -> int:
    if options.dashboard:
        return asyncio.run(cli.run_dashboard())
    if options.tray_status:
        return asyncio.run(cli.run_tray_status())
    if options.diagnostics:
        return asyncio.run(cli.run_diagnostics())
    raise ValueError("expected local UI option")


def _parse_key_value_options(values: Sequence[str] | None) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values or ():
        key, separator, item_value = value.partition("=")
        if not separator or not key.strip():
            raise ValueError("--skill-input values must use KEY=VALUE")
        parsed[key.strip()] = item_value
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())
