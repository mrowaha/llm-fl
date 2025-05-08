from agents import OpenAIChatCompletionsModel, AsyncOpenAI
qwen_code_model_id = 'qwen2.5-coder:7b'
qwen_code_model = OpenAIChatCompletionsModel(
    model=qwen_code_model_id,
    openai_client=AsyncOpenAI(
        base_url="http://localhost:11434/v1", api_key="ollama")
)
