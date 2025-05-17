# test_git_operations.py
import pytest
from git import Repo
from services.git_service import GitOperations


@pytest.fixture(scope="module")
def test_repo(tmp_path_factory):
    """Fixture that creates a test repository with commits"""
    repo_path = tmp_path_factory.mktemp("test_repo")
    repo = Repo.init(repo_path)

    # Create initial commit
    readme = repo_path / "README.md"
    readme.write_text("# Test Repository")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")

    # Create base branch
    repo.create_head("base-branch")

    # Create and switch to test branch
    repo.create_head("test-branch")
    repo.heads["test-branch"].checkout()

    # Make changes in test branch
    new_file = repo_path / "new_file.txt"
    new_file.write_text("Test content")
    repo.index.add(["new_file.txt"])
    repo.index.commit("Add new file")

    return repo_path


@pytest.fixture
def git_ops(test_repo):
    """Fixture providing GitOperations instance"""
    return GitOperations(test_repo)


def test_checkout_branch(git_ops):
    """Test branch checkout functionality"""
    git_ops.checkout_branch("test-branch")
    assert git_ops.repo.active_branch.name == "test-branch"

    git_ops.checkout_branch("base-branch")
    assert git_ops.repo.active_branch.name == "base-branch"


def test_get_changed_files(git_ops):
    """Test detection of changed files between branches"""
    changed_files = git_ops.get_changed_files("base-branch", "test-branch")
    assert "new_file.txt" in changed_files
    assert "README.md" not in changed_files  # Shouldn't show unchanged files


def test_get_commit_messages(git_ops):
    """Test retrieval of commit messages"""
    messages = git_ops.get_commit_messages("base-branch", "test-branch")
    assert len(messages) == 1
    assert "Add new file" in messages[0]


def test_empty_diff(git_ops):
    """Test when comparing identical branches"""
    changed_files = git_ops.get_changed_files("test-branch", "test-branch")
    assert changed_files == [""]

    messages = git_ops.get_commit_messages("test-branch", "test-branch")
    assert messages == []
