from tools.github_tool import GitHubTool

tool = GitHubTool()

repo = tool.get_repository_data(
    "https://github.com/langchain-ai/langgraph"
)

print(repo["name"])
print(repo["owner"])
print(repo["language"])
print(repo["description"])

print("\nREADME Preview\n")
print(repo["readme"][:500])