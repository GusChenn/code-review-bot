from github import Github, GithubException


class GithubPRFetcher:
    """
    Class responsible for fetching the latest pull requests from a Github repository.
    """

    def __init__(self, repo_name, gh_token):
        """
        Initialize GithubPRFetcher with repository name and Github token.
        """
        try:
            self.repo_name = repo_name
            self.gh_token = gh_token
            self.g = Github(self.gh_token)
            self.repo = self.g.get_repo(self.repo_name)
        except GithubException as e:
            print(f"Error initializing Github object: {e}")
            raise

    def get_latest_pr(self):
        """
        Fetch the latest pull request from the repository.
        """
        try:
            prs = self.repo.get_pulls(state="open", sort="created")
            return prs[0] if prs.totalCount > 0 else None
        except GithubException as e:
            print(f"Error fetching pull requests: {e}")
            return None
