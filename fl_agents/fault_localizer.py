import re
import json
from agents import Agent, Runner
from agents.tool import FunctionTool
from agents.run_context import RunContextWrapper
from openai.types.responses.response_input_item_param import Message

from fl_agents.hooks.base_agent import base_agent_hook
from fl_agents.tools.language_support import function_explanation_tool, class_method_explanation_tool
from fl_agents.tools.files_support import tool__load_file
from models import deepseek_chat_model as coverage_analyzer_model
# from models import qwen_code_model as fault_localizer_model
from prompts import localize_fault_prompt, system_prompt_editor
from fl_agents.coverage_analyzer import coverage_analyzer_agent


async def tool__load_file_from_agent(run_context: RunContextWrapper, str_args) -> str:
    args = json.loads(str_args)
    file_path = args['file_path']
    file_content = await tool__load_file(run_context, str_args)
    file_content_prompt = f"""
    here is the following file, that you should examine and shorten based on the rules
    {file_content}
    """

    result = await Runner.run(
        starting_agent=coverage_analyzer_agent,
        input=[
            Message(
                role="system",
                type="message",
                content=[
                    {
                        'text': system_prompt_editor,
                        'type': 'input_text'
                    }
                ]
            ),
            Message(
                role='user',
                type='message',
                content=[
                    {
                        'text': file_content_prompt,
                        'type': 'input_text'
                    }
                ]
            )
        ]
    )

    final_output = result.final_output_as(str)
    match = re.search(r"<file_content>(.*?)</file_content>",
                      final_output, re.DOTALL)
    if match:
        modified_response = f"<file_content file_path=\"{file_path}\">{match.group(1)}\n</file_content>"
        return modified_response
    return "an error occured extracting results"

file_content_tool = FunctionTool(
    name="get_file_content",
    description="gets the file content specified by the file path",
    params_json_schema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "file path to get the file content of"
                    }
                }
    },
    on_invoke_tool=tool__load_file_from_agent
)


fault_localizer_agent = Agent(
    model=coverage_analyzer_model,
    name="Fault Localizer Agent",
    instructions=localize_fault_prompt,
    tools=[
        file_content_tool,
        function_explanation_tool,
        class_method_explanation_tool,
    ],
    hooks=base_agent_hook
)
