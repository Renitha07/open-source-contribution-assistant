import json

from prompts.repository_understanding import SYSTEM_PROMPT
from schemas.repository_schema import RepositoryUnderstanding
from state.graph_state import GraphState
from utils.llm_service import invoke_llm


def repository_understanding_node(state: GraphState):

    response = invoke_llm(
        SYSTEM_PROMPT,
        state["repository"]["readme"],
    )

    data = json.loads(response)

    validated = RepositoryUnderstanding.model_validate(data)

    state["repository_understanding"] = validated.model_dump()

    state["execution"]["current_stage"] = "repository_understood"

    return state