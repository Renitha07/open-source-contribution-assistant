from tools.github_tool import GitHubTool

tool = GitHubTool()

repo = tool.get_repository_data(
    "https://github.com/langchain-ai/langgraph"
)

print("=" * 60)
print("Repository")
print("=" * 60)

print("Name:", repo["name"])
print("Owner:", repo["owner"])
print("Language:", repo["language"])
print("Stars:", repo["stars"])
print("Forks:", repo["forks"])
print("Open Issues:", repo["open_issues"])

print("\n")

print("=" * 60)
print("Top Level Structure")
print("=" * 60)

structure = tool.get_directory_structure(
    "https://github.com/langchain-ai/langgraph"
)

for item in structure:
    print(f"{item['type']:>4}  {item['name']}")