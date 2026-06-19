from __future__ import annotations

import asyncio
from argparse import ArgumentParser
from collections.abc import Sequence
from pathlib import Path

from private_ai_companion import PROJECT_NAME, __version__
from private_ai_companion.avatar import AvatarExpression
from private_ai_companion.bootstrap import ApplicationConfigPaths, create_application
from private_ai_companion.ui import RichCliApp


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
        )
    )
    if single_action_count > 1:
        parser.error(
            "--once, --voice-file, --avatar-expression and --screen-context "
            "are exclusive"
        )

    cli = RichCliApp(
        application=create_application(
            config_paths=ApplicationConfigPaths(
                persona=options.persona_config,
                providers=options.providers_config,
                speech=options.speech_config,
                avatar=options.avatar_config,
                privacy=options.privacy_config,
            ),
        )
    )
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

    return asyncio.run(cli.run_interactive())


if __name__ == "__main__":
    raise SystemExit(main())
