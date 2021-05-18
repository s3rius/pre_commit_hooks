from pathlib import Path

import mock

from pre_commit_hooks.commit_msg_prefix.entry import (
    get_ticket,
    main,
    update_message,
)


@mock.patch("pre_commit_hooks.commit_msg_prefix.entry.get_branch_name")
def test_branch_detection(branch_mock: mock.MagicMock) -> None:
    """
    Test ticket name detection.

    :param branch_mock: get_branch_name mock.
    """
    branch_mock.return_value = "MEME-123"
    assert get_ticket() == "MEME-123"

    branch_mock.return_value = "A-123"
    assert get_ticket() is None

    branch_mock.return_value = "meme-123"
    assert get_ticket() is None


def test_update_file_success(tmp_path: Path) -> None:
    """Test appending prefix.

    :param tmp_path: temporary directory.
    """
    commit_file = tmp_path / "COMMITMSG"
    commit_file.write_text("\nCommit message")
    update_message(
        commit_file=commit_file,
        prefix="TEST:",
        forced=False,
    )
    assert commit_file.read_text() == "TEST: \nCommit message"


def test_existing_prefix(tmp_path: Path) -> None:
    """Test skip adding if prefix exists.

    :param tmp_path: temporary directory.
    """
    commit_file = tmp_path / "COMMITMSG"
    commit_file.write_text("\nTEST: Commit message")
    update_message(
        commit_file=commit_file,
        prefix="TEST:",
        forced=False,
    )
    assert commit_file.read_text() == "\nTEST: Commit message"


def test_existing_prefix_forced(tmp_path: Path) -> None:
    """Test if prefix exists and addition is forced.

    :param tmp_path: path to temporary directory.
    """
    commit_file = tmp_path / "COMMITMSG"
    commit_file.write_text("\nTEST: Commit message")
    update_message(
        commit_file=commit_file,
        prefix="TEST:",
        forced=True,
    )
    assert commit_file.read_text() == "TEST: \nTEST: Commit message"


@mock.patch("pre_commit_hooks.commit_msg_prefix.entry.get_branch_name")
def test_success_without_ticket(
    branch_mock: mock.MagicMock,
    tmp_path: Path,
) -> None:
    """
    Test that it won't modiy a message not on a ticket branch.

    :param branch_mock: mock for branch name.
    :param tmp_path: path to tmp directory.
    """
    branch_mock.return_value = "NOT-A-TICKET"
    commit_file = tmp_path / "COMMITMSG"
    commit_file.write_text("Commit message")
    main(["-f={}::", str(commit_file)])  # noqa: P103
    assert commit_file.read_text() == "Commit message"


@mock.patch("pre_commit_hooks.commit_msg_prefix.entry.get_branch_name")
def test_success(
    branch_mock: mock.MagicMock,
    tmp_path: Path,
) -> None:
    """Test success case for the hole hook.

    :param branch_mock: mock for branch name.
    :param tmp_path: path to tmp directory.
    """
    branch_mock.return_value = "TICKET-123"
    commit_file = tmp_path / "COMMITMSG"
    commit_file.write_text("Commit message")
    main(["-f=::{}::", str(commit_file)])  # noqa: P103
    assert commit_file.read_text() == "::TICKET-123:: Commit message"
