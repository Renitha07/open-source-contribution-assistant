from utils.llm_service import invoke_llm
result = invoke_llm('Return only JSON: {"test": "ok"}', 'test')
print(result)