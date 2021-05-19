import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path
from typing import List, Optional

from pre_commit_hooks.utils.git import get_current_ticket


def parse_args(cli_args: List[str]) -> Namespace:
    """
    Parse CLI arguments.

    :param cli_args: arguments from cli.
    :return: Namespace for parsed arguments.
    """
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "commit_msg_file",
        type=Path,
        help="Path to COMMIT_EDITMSGD file (provided by pre-commit).",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="{}:",  # noqa: P103
        help="Commit prefix format.",
        dest="format",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force prefix addition.",
        dest="force",
    )
    return parser.parse_args(cli_args)


def update_message(commit_file: Path, prefix: str, forced: bool) -> None:
    """
    Update commit message.

    :param commit_file: path to commitmsg file.
    :param prefix: prefix to append.
    :param forced: append prefix even if it exists.
    """
    commit_msg = commit_file.read_text()

    if commit_msg.strip().startswith(prefix) and not forced:
        return

    with open(commit_file, "w") as commitmsg_file:
        commitmsg_file.write(f"{prefix} {commit_msg}")


def main(cli_args: Optional[List[str]] = None) -> None:
    """
    Main entry for commit message prefix.

    :param cli_args: cli arguments for tests.
    """
    if cli_args is None:
        cli_args = sys.argv[1:]
    args = parse_args(cli_args)
    ticket = get_current_ticket()
    if ticket is None:
        return
    prefix = args.format.format(ticket)
    update_message(args.commit_msg_file, prefix, args.force)
