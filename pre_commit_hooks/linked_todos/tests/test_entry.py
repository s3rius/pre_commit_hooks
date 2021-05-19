from pathlib import Path

import mock
import pytest

from pre_commit_hooks.linked_todos.entry import find_todos, main


def test_find_todos(tmp_path: Path) -> None:
    """
    Test finding todos.

    :param tmp_path: temporary test dir.
    """
    tmp_file = tmp_path / "test"
    tmp_file.write_text("Test # TODO ATASK-12:")
    todos = find_todos(tmp_file, "ATASK-12")
    assert len(todos) == 1

    tmp_file.write_text("Test # TODO AATASK-12:")
    todos = find_todos(tmp_file, "ATASK-12")
    assert not todos

    tmp_file.write_text("Test #   TODO ATASK-12   :")
    todos = find_todos(tmp_file, "ATASK-12")
    assert len(todos) == 1

    tmp_file.write_text("# TODO TTT-123: AND TODO TTT-123:")
    todos = find_todos(tmp_file, "TTT-123")
    assert len(todos) == 1


@mock.patch("pre_commit_hooks.linked_todos.entry.list_all_git_files")
def test_main_not_a_task_branch(
    list_files_mock: mock.MagicMock,
    active_branch: mock.MagicMock,
    tmp_path: Path,
) -> None:
    """
    Test that hook will exit normally if it's a not a ticket branch.

    :param list_files_mock: git repo files mock.
    :param active_branch: current branch mock.
    :param tmp_path: temporary directory.
    """
    active_branch.return_value = "NOT-A-TASK"
    file1 = tmp_path / "file1"

    list_files_mock.return_value = [file1]

    main()


@mock.patch("pre_commit_hooks.linked_todos.entry.list_all_git_files")
def test_main_success(
    list_files_mock: mock.MagicMock,
    active_branch: mock.MagicMock,
    tmp_path: Path,
) -> None:
    """
    Test that hook will exit normally if it's a not a ticket branch.

    :param list_files_mock: git repo files mock.
    :param active_branch: current branch mock.
    :param tmp_path: temporary directory.
    """
    active_branch.return_value = "TASK-123"

    file1 = tmp_path / "file1"
    file2 = tmp_path / "file2"
    file1.write_text("Test\n\t# TODO TASK-123: do something.")
    file2.write_text("# TODO TASK-123: write something.")

    list_files_mock.return_value = [file1, file2]

    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1
