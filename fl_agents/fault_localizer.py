import os
import pathlib
import json
from agents import Agent
from agents.tool import FunctionTool
from fl_agents.hooks.fault_localizer import fault_localizer_agent_hook
from agents.run_context import RunContextWrapper
from fl_agents.language_support import class_method_explanation_agent, function_explanation_agent, function_explanation_tool, class_method_explanation_tool
from dirs import get_minified_annotations_folder, get_project_bug_dir
from models import deepseek_chat_model as fault_localizer_model
# from models import qwen_code_model as fault_localizer_model
from prompts import localize_fault_prompt


async def tool__load_file(run_context: RunContextWrapper, str_args) -> str:
    args = json.loads(str_args)
    project_name = run_context.context['project_name']
    bug_id = run_context.context['bug_id']
    file = args['file_path']
    minified_annotations_dir = get_minified_annotations_folder(
        project_name, bug_id)

    file_content: str = ""
    with open(
        os.path.join(str(minified_annotations_dir), file+',cover')
    ) as f:
        file_content = f.read()

    return f"""
    <file_executed_content file={args['file_path']}>
    {file_content}
    </file_executed_content>
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

executed_files_tool = FunctionTool(
    name="get_executed_file_content",
    description="gets the executed parts of the failing test file script",
    params_json_schema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "file path in which the class is housed in"
                    }
                }
    },
    on_invoke_tool=tool__load_file
)

fault_localizer_agent = Agent(
    model=fault_localizer_model,
    name="Fault Localizer Agent",
    instructions=localize_fault_prompt,
    tools=[
        executed_files_tool,
        function_explanation_tool,
        class_method_explanation_tool
    ],
    hooks=fault_localizer_agent_hook
)
