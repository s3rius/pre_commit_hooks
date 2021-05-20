import mock

from pre_commit_hooks.utils.git import get_current_ticket


@mock.patch("pre_commit_hooks.utils.git.get_active_branch_name")
def test_branch_detection(branch_mock: mock.MagicMock) -> None:
    """
    Test ticket name detection.

    :param branch_mock: get_branch_name mock.
    """
    branch_mock.return_value = "MEME-123"
    assert get_current_ticket() == "MEME-123"

    branch_mock.return_value = "A-123"
    assert get_current_ticket() is None

    branch_mock.return_value = "meme-123"
    assert get_current_ticket() is None

    branch_mock.return_value = None
    assert get_current_ticket() is None
