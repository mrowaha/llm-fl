import os
from agents import OpenAIChatCompletionsModel, AsyncOpenAI
deepseek_chat_model_id = 'deepseek-chat'
deepseek_chat_model = OpenAIChatCompletionsModel(
    model=deepseek_chat_model_id,
    openai_client=AsyncOpenAI(
        base_url="https://api.deepseek.com", api_key=os.getenv("DEEPSEEK_API_KEY"))
)

deepseek_r1_model_id = 'MFDoom/deepseek-r1-tool-calling:7b'
deepseek_r1_model = OpenAIChatCompletionsModel(
    model=deepseek_r1_model_id,
    openai_client=AsyncOpenAI(
        base_url="http://localhost:11434/v1", api_key="ollama")
)
