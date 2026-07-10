import base64
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()


class GitHubTool:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.session = requests.Session()

        github_token = os.getenv("GITHUB_TOKEN")

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "OpenSourceContributionAssistant",
        }

        if github_token:
            headers["Authorization"] = f"Bearer {github_token}"

        self.session.headers.update(headers)

    def _request(self, endpoint: str, params: dict | None = None):
        """
        Generic GitHub API request helper.
        """

        url = f"{self.BASE_URL}{endpoint}"

        response = self.session.get(url, params=params)

        response.raise_for_status()

        return response.json()

    def parse_repo_url(self, repo_url: str):
        parsed = urlparse(repo_url)

        if parsed.netloc != "github.com":
            raise ValueError("Invalid GitHub repository URL")

        parts = parsed.path.strip("/").split("/")

        if len(parts) < 2:
            raise ValueError("Repository URL must include owner and repository name")

        owner = parts[0]
        repo = parts[1]

        return owner, repo

    def _fetch_repository(self, owner: str, repo: str):
        return self._request(f"/repos/{owner}/{repo}")

    def _fetch_readme(self, owner: str, repo: str):
        data = self._request(f"/repos/{owner}/{repo}/readme")

        return base64.b64decode(data["content"]).decode("utf-8")

    def _fetch_directory_tree(self, owner: str, repo: str, branch: str):
        tree = self._request(
            f"/repos/{owner}/{repo}/git/trees/{branch}",
            params={"recursive": "1"},
        )

        return tree["tree"]

    def get_repository_data(self, repo_url: str):
        owner, repo = self.parse_repo_url(repo_url)

        repository = self._fetch_repository(owner, repo)

        readme = self._fetch_readme(owner, repo)

        directory_tree = self._fetch_directory_tree(
            owner,
            repo,
            repository["default_branch"],
        )

        return {
            "name": repository["name"],
            "owner": repository["owner"]["login"],
            "description": repository["description"],
            "language": repository["language"],
            "default_branch": repository["default_branch"],
            "stars": repository["stargazers_count"],
            "forks": repository["forks_count"],
            "open_issues": repository["open_issues_count"],
            "readme": readme,
            "directory_tree": directory_tree,
        }

    def get_directory_structure(self, repo_url: str):
        repository = self.get_repository_data(repo_url)

        top_level = []

        for item in repository["directory_tree"]:
            path = item["path"]

            if "/" not in path:
                top_level.append(
                    {
                        "name": path,
                        "type": item["type"],
                    }
                )

        return sorted(top_level, key=lambda x: (x["type"], x["name"]))

    def get_issues(self, repo_url: str, labels: list[str] | None = None, max_issues: int = 50):
        """
        Fetch issues from a repository.
        
        Args:
            repo_url: GitHub repository URL
            labels: Optional list of labels to filter by (e.g., ["good first issue", "help wanted"])
            max_issues: Maximum number of issues to fetch
            
        Returns:
            List of issue dictionaries
        """
        owner, repo = self.parse_repo_url(repo_url)
        
        params = {
            "state": "open",
            "sort": "created",
            "direction": "desc",
            "per_page": min(max_issues, 100),
        }
        
        if labels:
            params["labels"] = ",".join(labels)
        
        issues = self._request(f"/repos/{owner}/{repo}/issues", params=params)
        
        # Filter out pull requests (they appear in issues API)
        issues = [issue for issue in issues if "pull_request" not in issue]
        
        # Simplify issue data
        simplified = []
        for issue in issues[:max_issues]:
            simplified.append({
                "number": issue["number"],
                "title": issue["title"],
                "url": issue["html_url"],
                "labels": [label["name"] for label in issue["labels"]],
                "created_at": issue["created_at"],
                "comments": issue["comments"],
                "body": issue["body"] or "",
            })
        
        return simplified
    
    