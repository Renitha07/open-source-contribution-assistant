from typing import TypedDict, NotRequired


class RepositoryState(TypedDict):
    name: str
    owner: str
    description: str
    language: str
    default_branch: str
    readme: str


class RepositoryUnderstandingState(TypedDict):
    purpose: str
    summary: str
    technologies: list[str]
    beginner_explanation: str


class ExecutionState(TypedDict):
    current_stage: str
    status: str
    error: NotRequired[str]



class GraphState(TypedDict):
    repository_url: str

    repository: RepositoryState
    repository_understanding: RepositoryUnderstandingState

    execution: ExecutionState