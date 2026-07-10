import json

from prompts.architecture_analysis import SYSTEM_PROMPT
from schemas.architecture_schema import ArchitectureAnalysis
from utils.llm_service import invoke_llm


def architecture_node(state):

    repository = state["repository"]

    directory = repository["directory_tree"]

    prompt = f"""
Repository Description

{repository["description"]}


README

{repository["readme"][:8000]}


Directory Structure

{directory}
"""

    response = invoke_llm(
        SYSTEM_PROMPT,
        prompt,
    )

    data = json.loads(response)

    validated = ArchitectureAnalysis.model_validate(data)

    state["architecture"] = validated.model_dump()

    state["execution"]["current_stage"] = "architecture_completed"

    return state