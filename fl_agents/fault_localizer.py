import os
import pathlib
import json
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.tool import FunctionTool
from fl_agents.hooks.fault_localizer import fault_localizer_agent_hook
from agents.run_context import RunContextWrapper
from fl_agents.language_support import class_method_explanation_agent, function_explanation_agent
from dirs import get_minified_annotations_folder, get_project_bug_dir


async def tool__load_failing_test_file(run_context: RunContextWrapper, args) -> str:
    project_name = run_context.context['project_name']
    bug_id = run_context.context['bug_id']
    failing_test_file = run_context.context['failing_test_file']
    minified_annotations_dir = get_minified_annotations_folder(
        project_name, bug_id)

    file_content: str = ""
    with open(
        os.path.join(str(minified_annotations_dir), failing_test_file)
    ) as f:
        file_content = f.read()

    return f"""
    <failing_test_file_content>
    {file_content}
    </failing_test_file_content>
    """


async def tool__load_executed_files(run_context: RunContextWrapper, args) -> str:
    project_name = run_context.context['project_name']
    bug_id = run_context.context['bug_id']

    bug_executed_files_path = get_project_bug_dir(
        project_name, bug_id, 'data') / pathlib.Path('executed-files.json')

    executed_files = []
    with open(bug_executed_files_path, 'r') as f:
        executed_files = json.load(f)

    return f"""
    <executed_files>
    {executed_files}
    </executed_files>
    """


fault_localizer_model_id = 'qwen2.5:7b-instruct-8k'
fault_localizer_model = OpenAIChatCompletionsModel(
    model=fault_localizer_model_id,
    openai_client=AsyncOpenAI(
        base_url="http://localhost:11434/v1", api_key="ollama")

)


fault_localizer_agent = Agent(
    model=fault_localizer_model,
    name="Fault Localizer Agent",
    instructions=f"""
    {RECOMMENDED_PROMPT_PREFIX}
    <your role>
    You are a debugging assistant. Your job will be to study a reason behind a failing
    test provided to you. You should do the following:
    1. Load the failing test content from the tool available to you
    2. Load the executed files from the tool available to you
    3. Trace the code by making meaningful searches for functions or class methods recursively
    4. You cannot finish until you make a guess about why the test was failing
    Your tracing searches should only be limited to the executed files
    """,
    handoff_description="""
    Will take the failing test and begin fault localizing
    """,
    handoffs=[
        function_explanation_agent,
        class_method_explanation_agent
    ],
    tools=[
        FunctionTool(
            name="get_failing_test_file_content",
            description="gets the failing content of the failing test",
            params_json_schema={
                "type": "object",
                "properties": {}
            },
            on_invoke_tool=tool__load_failing_test_file
        ),
        FunctionTool(
            name="get_executed_files",
            description="gets the executed files in the failing test coverage",
            params_json_schema={
                "type": "object",
                "properties": {}
            },
            on_invoke_tool=tool__load_executed_files
        )
    ],
    hooks=fault_localizer_agent_hook
)
