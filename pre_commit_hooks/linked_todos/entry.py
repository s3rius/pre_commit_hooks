import re
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
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
        "files",
        nargs="*",
        default=[],
        help="Files to parse for linked todos (Provided by pre-commit).",
    )

    return parser.parse_args(cli_args)


def find_todos(filename: str, ticket: str) -> List[str]:  # noqa: WPS210
    """Find todos lined to ticket.

    The format is:

    "TODO {ticket}:"

    :param filename: file to parse.
    :param ticket: current_ticket
    :return: list of found linked todos.
    """
    with open(filename) as source_file:
        source_lines = source_file.readlines()

    todo_regex = re.compile(rf"TODO\s+\b{ticket}\b\s*:")

    todos = []

    for index, line in enumerate(source_lines):
        line_num = index + 1
        if todo_regex.findall(line):
            todos.append(f"./{filename}:{line_num}")

    return todos


def main(cli_args: Optional[List[str]] = None) -> None:  # noqa: WPS210
    """
    Main entry for parsing linked todos.

    :param cli_args: cli arguments for tests.
    """
    ticket = get_current_ticket()

    if cli_args is None:
        cli_args = sys.argv[1:]

    if ticket is None:
        return

    todos = []
    args = parse_args(cli_args)

    for src_file in args.files:
        todos.extend(find_todos(src_file, ticket))

    if todos:
        print("Found todos linked to current branch.")  # noqa: WPS421
        print("Remove them before commiting.")  # noqa: WPS421
        for todo in todos:
            print(todo)  # noqa: WPS421
        exit(1)  # noqa: WPS421
