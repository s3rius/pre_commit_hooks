from typing import Generator

import mock
import pytest


@pytest.fixture(scope="function")
def active_branch() -> Generator[mock.MagicMock, None, None]:
    """Mock getting active branch.

    :yield: mock
    """
    with mock.patch("pre_commit_hooks.utils.git.get_active_branch_name") as fmock:
        yield fmock
