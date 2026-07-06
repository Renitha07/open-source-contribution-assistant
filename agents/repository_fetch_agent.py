from state.graph_state import GraphState
from tools.github_tool import GitHubTool

github_tool = GitHubTool()


def repository_fetch_node(state: GraphState):

    repository = github_tool.get_repository_data(
        state["repository_url"]
    )

    state["repository"] = repository

    state["execution"]["current_stage"] = "repository_fetched"

    return state