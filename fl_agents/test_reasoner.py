from pathlib import Path

from agents.tool import FunctionTool
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.run_context import RunContextWrapper
from dirs import get_project_bug_dir
from fl_agents.hooks.test_reasoner import test_reasoner_agent_hook
from fl_agents.fault_localizer import fault_localizer_agent


# Agentic Tools
async def tool__get_failing_test(run_context: RunContextWrapper, args: str) -> str:
    project_name = run_context.context['project_name']
    bug_id = run_context.context['bug_id']
    failing_test: str = ""
    with open(get_project_bug_dir(project_name, bug_id, 'data') / Path('failing_test.txt')) as f:
        failing_test = f.read()
    print(failing_test)
    return failing_test

# test_reasoner_model_id = 'deepseek-r1:8b'
test_reasoner_model_id = 'qwen2.5:7b-instruct-8k'
test_reasoner_model = OpenAIChatCompletionsModel(
    model=test_reasoner_model_id,
    openai_client=AsyncOpenAI(
        base_url="http://localhost:11434/v1", api_key="ollama")
)

failing_test_fetch_tool: FunctionTool = FunctionTool(
    name="get_failing_test",
    description="returns the content of the failing test",
    params_json_schema={
        "type": "object",
        "properties": {}
    },
    on_invoke_tool=tool__get_failing_test
)

test_reasoner_agent = Agent(
    name="Test Reasoning Agent",
    model=test_reasoner_model,
    instructions=f"""
            {RECOMMENDED_PROMPT_PREFIX}
            <your role>
            You are an assistant who will explain the reason behind a failing test.
            1. First get the failing test from the tool available to you
            2. Explain the failing test
            3. Forward it to agent who can take this explanation and start fault localization
            """,
    handoffs=[fault_localizer_agent],
    tools=[failing_test_fetch_tool],
    hooks=test_reasoner_agent_hook
)
