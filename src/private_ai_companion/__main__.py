from __future__ import annotations

import asyncio
from argparse import ArgumentParser
from collections.abc import Sequence

from private_ai_companion import PROJECT_NAME, __version__
from private_ai_companion.bootstrap import create_application


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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    options = parser.parse_args(argv)

    if bool(options.version):
        print(f"{PROJECT_NAME} {__version__}")
        return 0

    application = create_application()
    snapshot = asyncio.run(application.run_once())

    print(PROJECT_NAME)
    print(f"Runtime lifecycle completed with state: {snapshot.state.phase.value}.")
    print("Interactive text UI will be implemented in Phase 03.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
