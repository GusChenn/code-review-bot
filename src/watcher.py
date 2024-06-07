import time
from src.code_review_fetcher import GithubCodeReviewer
from src.pull_request_fetcher import GithubPRFetcher


class GithubWatcher:
    """
    Class responsible for watching a Github repository for new pull requests and reviewing them.
    """

    def __init__(self, repo_name, gh_token, openai_key):
        """
        Initialize GithubWatcher with repository name, Github token, and OpenAI key.
        """
        self.pr_fetcher = GithubPRFetcher(repo_name, gh_token)
        self.reviewer = GithubCodeReviewer(openai_key)
        self.last_checked_pr = None

    def watch(self):
        """
        Continuously watch the repository for new pull requests and review them.
        """
        while True:
            try:
                latest_pr = self.pr_fetcher.get_latest_pr()
                if latest_pr is not None and latest_pr != self.last_checked_pr:
                    self.last_checked_pr = latest_pr
                    print(f"New PR found: {latest_pr.title}")
                    diffs = "\n".join(
                        [
                            file.patch
                            for file in latest_pr.get_files()
                            if isinstance(file.patch, str)
                        ]
                    )
                    review = self.reviewer.review_code(diffs)
                    print("Commenting on PR...")
                    latest_pr.create_issue_comment(
                        review
                    )  # post the review as a comment
                    print("Commented on PR!")
                time.sleep(10)  # sleep for 10 seconds before checking again
            except Exception as e:
                print(f"Error occurred while watching for PRs: {e}")
