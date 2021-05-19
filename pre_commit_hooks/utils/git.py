import re
from typing import Optional

import git

JIRA_TICKET_REGEXP = re.compile(r"[A-Z]{2,}\-\d+")


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
