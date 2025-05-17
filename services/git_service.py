# git_component/git_operations.py
from git import Repo


class GitOperations:
    def __init__(self, repo_path):
        self.repo = Repo(repo_path)

    def get_changed_files(self, base_branch, target_branch):
        """Get list of changed files between branches"""
        diff = self.repo.git.diff(
            f"{base_branch}..{target_branch}", name_only=True)
        return diff.split("\n")

    def get_commit_messages(self, base_branch, target_branch):
        """Get commit messages between branches"""
        commits = list(self.repo.iter_commits(
            f"{base_branch}..{target_branch}"))
        return [commit.message for commit in commits]

    def checkout_branch(self, branch_name):
        """Checkout specific branch"""
        self.repo.git.checkout(branch_name)
