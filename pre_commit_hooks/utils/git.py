import re
import subprocess
from pathlib import Path
from typing import List, Optional

import git

JIRA_TICKET_REGEXP = re.compile(r"[A-Z]{2,}\-\d+")


def list_all_git_files() -> List[Path]:
    """
    List all files in git repo that are not ignored.

    :return: List of files.
    """
    root_dir = Path(git.Repo(".", search_parent_directories=True).git_dir).parent
    relative_paths = subprocess.check_output(
        "git ls-files --full-name",
        cwd=str(root_dir),
        shell=True,
        encoding="utf-8",
    ).splitlines()
    return list(map(lambda path: root_dir / path, relative_paths))


def get_active_branch_name() -> str:
    """
    Get current branch name.

    :returns: active git branch.
    """
    return str(git.Repo(".").active_branch.name)


def get_current_ticket() -> Optional[str]:
    """Get JIRA ticket name.

    This function checks whether the current_branch name is
    a name of JIRA ticket.

    :return: name of branch if it's a JIRA ticket.
    """
    branch_name = get_active_branch_name()
    if JIRA_TICKET_REGEXP.match(branch_name):
        return branch_name
    return None
