from langgraph.graph import StateGraph, START, END

from state.graph_state import GraphState
from agents.repository_fetch_agent import repository_fetch_node
from agents.repository_understanding_agent import repository_understanding_node

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

builder.add_edge(
    "repository_understanding",
    END,
)

graph = builder.compile()