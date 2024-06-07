from github import Github
import time
from src.code_review_fetcher import CodeReviewer


class GithubWatcher:
    def __init__(self, repo_name, gh_token, openai_key):
        self.pr_fetcher = GithubPRFetcher(repo_name, gh_token)
        self.reviewer = CodeReviewer(openai_key)
        self.last_checked_pr = None

    def watch(self):
        while True:
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
                latest_pr.create_issue_comment(review)  # post the review as a comment
                print("Commented on PR!")
            time.sleep(10)  # sleep for 10 seconds before checking again
