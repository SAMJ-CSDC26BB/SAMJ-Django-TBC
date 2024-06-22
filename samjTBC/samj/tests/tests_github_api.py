import unittest

from samj.github.github_api import GitHubAPI


class TestGitHubAPI(unittest.TestCase):
    def test_github_token(self):
        api = GitHubAPI()  # Create an instance of GitHubAPI
        token = api.get_github_token()
        self.assertIsNotNone(token, f"GitHub token is not set: {token}")

    def test_github_list_repo_issues(self):
        api = GitHubAPI()
        issues = api.list_github_issues(self)
        print(issues.text)
        self.assertIsNotNone(issues, "Failed to list issues")


if __name__ == '__main__':
    unittest.main()
