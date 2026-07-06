from utils.llm_service import invoke_llm

response = invoke_llm(
    system_prompt="You are a helpful AI assistant.",
    user_prompt="Explain LangGraph in two sentences."
)

print(response)
