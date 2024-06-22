import os
import unittest


class TestGitHubAPI(unittest.TestCase):
    def test_github_token(self):
        token = os.getenv('GITHUB_TOKEN_SAMJ')
        self.assertIsNotNone(token, "GitHub token is not set")



if __name__ == '__main__':
    unittest.main()
