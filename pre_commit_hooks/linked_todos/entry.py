import re
from pathlib import Path
from typing import List

from pre_commit_hooks.utils.git import get_current_ticket, list_all_git_files


def find_todos(filename: Path, ticket: str) -> List[str]:  # noqa: WPS210
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


def main() -> None:  # : WPS210
    """Main entry for parsing linked todos."""
    ticket = get_current_ticket()

    if ticket is None:
        return

    todos = []

    for src_file in list_all_git_files():
        todos.extend(find_todos(src_file, ticket))

    if todos:
        print("Found todos linked to current branch.")  # noqa: WPS421
        print("Remove them before commiting.")  # noqa: WPS421
        for todo in todos:
            print(todo)  # noqa: WPS421
        exit(1)  # noqa: WPS421
