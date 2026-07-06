import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL_NAME = "nvidia/nemotron-3-ultra-550b-a55b"


def get_llm():
    return OpenAI(
        api_key=os.getenv("NVIDIA_API_KEY"),
        base_url="https://integrate.api.nvidia.com/v1",
    )