from graph.builder import graph

initial_state = {
    "repository_url": "https://github.com/langchain-ai/langgraph",

    "repository": {},

    "repository_understanding": {},

    "execution": {
        "current_stage": "start",
        "status": "running",
    },
}

result = graph.invoke(initial_state)

print("\n========== Repository Analysis ==========\n")

print(result["repository_understanding"]["purpose"])

print(result["repository_understanding"]["summary"])

print(result["repository_understanding"]["technologies"])

print(result["repository_understanding"]["beginner_explanation"])