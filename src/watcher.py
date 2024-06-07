from github import Github
import time
from src.code_review_fetcher import CodeReviewer


class GithubWatcher:
    def __init__(self, repo_name, gh_token, openai_key):
        self.repo_name = repo_name
        self.gh_token = gh_token
        self.g = Github(self.gh_token)
        self.repo = self.g.get_repo(self.repo_name)
        self.last_checked_pr = None
        self.reviewer = CodeReviewer(openai_key)

    def get_latest_pr(self):
        prs = self.repo.get_pulls(state="open", sort="created")
        return prs[0] if prs.totalCount > 0 else None

    def watch(self):
        while True:
            latest_pr = self.get_latest_pr()
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
