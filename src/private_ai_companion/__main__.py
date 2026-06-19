from __future__ import annotations

import asyncio
from argparse import ArgumentParser
from collections.abc import Sequence
from pathlib import Path

from private_ai_companion import PROJECT_NAME, __version__
from private_ai_companion.bootstrap import create_application
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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    options = parser.parse_args(argv)

    if bool(options.version):
        print(f"{PROJECT_NAME} {__version__}")
        return 0

    if options.once is not None and options.voice_file is not None:
        parser.error("--once and --voice-file cannot be used together")

    cli = RichCliApp(
        application=create_application(
            persona_config_path=options.persona_config,
            providers_config_path=options.providers_config,
            speech_config_path=options.speech_config,
        )
    )
    if options.once is not None:
        return asyncio.run(cli.run_single_turn(str(options.once)))
    if options.voice_file is not None:
        return asyncio.run(cli.run_voice_file(Path(options.voice_file)))

    return asyncio.run(cli.run_interactive())


if __name__ == "__main__":
    raise SystemExit(main())
