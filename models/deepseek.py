import os
from agents import OpenAIChatCompletionsModel, AsyncOpenAI
deepseek_chat_model_id = 'deepseek-chat'
deepseek_chat_model = OpenAIChatCompletionsModel(
    model=deepseek_chat_model_id,
    openai_client=AsyncOpenAI(
        base_url="https://api.deepseek.com", api_key=os.getenv("DEEPSEEK_API_KEY"))
)
