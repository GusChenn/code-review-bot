class GithubPRFetcher:
    def __init__(self, repo_name, gh_token):
        self.repo_name = repo_name
        self.gh_token = gh_token
        self.g = Github(self.gh_token)
        self.repo = self.g.get_repo(self.repo_name)

    def get_latest_pr(self):
        prs = self.repo.get_pulls(state="open", sort="created")
        return prs[0] if prs.totalCount > 0 else None
