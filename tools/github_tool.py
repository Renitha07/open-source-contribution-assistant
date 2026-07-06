import base64
from urllib.parse import urlparse

import requests


class GitHubTool:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.session = requests.Session()

    def parse_repo_url(self, repo_url: str):
        parsed = urlparse(repo_url)

        if parsed.netloc != "github.com":
            raise ValueError("Invalid GitHub URL")

        parts = parsed.path.strip("/").split("/")

        if len(parts) < 2:
            raise ValueError("Repository URL must include owner and repository name")

        return parts[0], parts[1]

    def _fetch_repository(self, owner: str, repo: str):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"

        response = self.session.get(url)
        response.raise_for_status()

        return response.json()

    def _fetch_readme(self, owner: str, repo: str):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/readme"

        response = self.session.get(url)
        response.raise_for_status()

        data = response.json()

        return base64.b64decode(data["content"]).decode("utf-8")

    def get_repository_data(self, repo_url: str):
        owner, repo = self.parse_repo_url(repo_url)

        repo_data = self._fetch_repository(owner, repo)
        readme = self._fetch_readme(owner, repo)

        return {
            "name": repo_data["name"],
            "owner": repo_data["owner"]["login"],
            "description": repo_data["description"],
            "language": repo_data["language"],
            "default_branch": repo_data["default_branch"],
            "readme": readme,
        }