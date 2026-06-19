from __future__ import annotations

import asyncio
from argparse import ArgumentParser
from collections.abc import Sequence

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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    options = parser.parse_args(argv)

    if bool(options.version):
        print(f"{PROJECT_NAME} {__version__}")
        return 0

    cli = RichCliApp(application=create_application())
    if options.once is not None:
        return asyncio.run(cli.run_single_turn(str(options.once)))

    return asyncio.run(cli.run_interactive())


if __name__ == "__main__":
    raise SystemExit(main())
