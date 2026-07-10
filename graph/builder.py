from langgraph.graph import StateGraph, START, END

from state.graph_state import GraphState
from agents.repository_fetch_agent import repository_fetch_node
from agents.repository_understanding_agent import repository_understanding_node
from agents.architecture_agent import architecture_node
from agents.issue_agent import issue_intelligence_node
from agents.planner_agent import planner_node
from agents.learning_agent import learning_node
from agents.report_agent import report_node

builder = StateGraph(GraphState)

builder.add_node(
    "repository_fetch",
    repository_fetch_node,
)

builder.add_node(
    "repository_understanding",
    repository_understanding_node,
)

builder.add_edge(
    START,
    "repository_fetch",
)

builder.add_edge(
    "repository_fetch",
    "repository_understanding",
)

builder.add_node(
    "architecture",
    architecture_node,
)

builder.add_edge(
    "repository_understanding",
    "architecture",
)

builder.add_node(
    "issue_intelligence",
    issue_intelligence_node,
)

builder.add_edge(
    "architecture",
    "issue_intelligence",
)

builder.add_node(
    "planner",
    planner_node,
)

builder.add_edge(
    "issue_intelligence",
    "planner",
)

builder.add_node(
    "learning",
    learning_node,
)

builder.add_edge(
    "planner",
    "learning",
)

builder.add_node(
    "report",
    report_node,
)

builder.add_edge(
    "learning",
    "report",
)

builder.add_edge(
    "report",
    END,
)

graph = builder.compile()