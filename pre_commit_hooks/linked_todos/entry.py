import re
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path
from typing import List, Optional

from pre_commit_hooks.utils.git import get_current_ticket, list_all_git_files


def parse_args(cli_args: Optional[List[str]]) -> Namespace:
    """Parse CLI arguments.

    :param cli_args: test cli arguments.
    :return: parsed namespace.
    """
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--disable-todos",
        action="store_true",
        default=False,
        help="Disable todo detection.",
    )

    parser.add_argument(
        "formats",
        nargs="*",
        type=str,
        default=[],
        help="List of different formats for special comments. E.G FIXME.",
    )

    return parser.parse_args(cli_args)


def find_todos(  # noqa: WPS210
    filename: Path,
    ticket: str,
    additional_formats: List[str],
    disable_todos: bool,
) -> List[str]:  # : WPS210
    """Find todos lined to ticket.

    The format is:

    "TODO {ticket}:"

    :param filename: file to parse.
    :param ticket: current_ticket
    :param additional_formats: additional search strings as FIXME e.t.c.
    :param disable_todos: disable TODO search.
    :return: list of found linked todos.
    """
    with open(filename) as source_file:
        try:
            source_lines = source_file.readlines()
        except UnicodeDecodeError:
            return []

    if not disable_todos:
        additional_formats.append("TODO")

    formats_regex = "|".join(additional_formats)

    todo_regex = re.compile(rf"({formats_regex})\s+\b{ticket}\b\s*:")

    todos = []

    for index, line in enumerate(source_lines):
        line_num = index + 1
        if todo_regex.findall(line):
            todos.append(f"{filename}:{line_num}")

    return todos


def main(cli_args: Optional[List[str]] = None) -> None:  # : WPS210
    """
    Main entry for parsing linked todos.

    :param cli_args: cli arguments for testing.
    """
    args = parse_args(cli_args)

    ticket = get_current_ticket()

    if ticket is None:
        return

    todos = []

    for src_file in list_all_git_files():
        todos.extend(
            find_todos(
                src_file,
                ticket,
                args.formats,
                args.disable_todos,
            ),
        )

    if todos:
        print("Found todos linked to current branch.")  # noqa: WPS421
        print("Remove them before commiting.")  # noqa: WPS421
        for todo in todos:
            print(todo)  # noqa: WPS421
        exit(1)  # noqa: WPS421
