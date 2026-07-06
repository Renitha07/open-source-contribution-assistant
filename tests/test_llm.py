from config.llm import get_llm

client = get_llm()

response = client.chat.completions.create(
    model="nvidia/llama-3.3-nemotron-super-49b-v1",
    messages=[
        {
            "role": "user",
            "content": "Say hello and what are you doing in one sentence."
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)