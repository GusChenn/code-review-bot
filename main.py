from dotenv import load_dotenv
import os
from src.watcher import GithubWatcher


def main():
    load_dotenv()
    repo_name = os.getenv("GH_REPO_NAME")
    gh_token = os.getenv("GH_TOKEN")
    openai_key = os.getenv("OPENAI_KEY")

    watcher = GithubWatcher(repo_name, gh_token, openai_key)
    watcher.watch()


if __name__ == "__main__":
    main()
