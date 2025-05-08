import sys
import os

if len(sys.argv) != 3:
    print('please specify the project name and the bug id')
    os._exit(1)

import asyncio
import json
from openai.types.responses.response_input_item_param import Message
from agents import Runner, ItemHelpers
from fl_agents.fault_localizer import fault_localizer_agent
from fl_agents.hooks import fault_localization_run_hook
from fl_agents.coverage_analyzer import coverage_analyzer_agent
from openai.types.responses import ResponseTextDeltaEvent
from dirs import get_project_bug_dir
from prompts import system_prompt_fl, system_prompt_editor
from log import Logger as RunLogger, NoNewlineFormatter


project = sys.argv[1]
bug = int(sys.argv[2])
_logger = RunLogger("fl.Run").configure(
    logging_formatter=NoNewlineFormatter()
).get_logger()


async def main():
    global project, bug

    project_dir = get_project_bug_dir(
        project_name=project, bug_id=bug, type='data')

    failing_test = ''
    with open(project_dir / 'failing_test.txt', 'r') as f:
        failing_test = f.readlines()
    failing_test_prompt = f"""
    <failing_test_output>
    {failing_test}
    </failing_test_output>
    """.strip()

    executed_lines = []
    with open(project_dir / 'executed-files.json', 'r') as f:
        executed_lines = json.load(f)
    executed_lines_prompt = f"""
    <project_executed_files>
    {executed_lines}
    </project_executed_files>
    """.strip()

    # fl_prompt = f"""
    # {failing_test_prompt}

    # {executed_lines_prompt}
    # """

    fl_prompt = "I need you to explain me the file contents of thefuck/output_readers/shell_logger.py"

    result = Runner.run_streamed(
        input=[
            # Message(
            #     role="system",
            #     type="message",
            #     content=[
            #         {
            #             'text': system_prompt_fl,
            #             'type': 'input_text'
            #         }
            #     ]
            # ),
            Message(
                role="user",
                type="message",
                content=[
                    {
                        'text': fl_prompt,
                        'type': 'input_text'
                    }
                ]
            )
        ],
        starting_agent=fault_localizer_agent,
        context={
            "project_name": project,
            "bug_id": bug,
        },
        hooks=fault_localization_run_hook
    )

    with open(get_project_bug_dir(project, bug, 'data') / 'fl-run.txt', 'w') as f:
        print("=== Run starting ===\n\n")

        async for event in result.stream_events():
            pass
            # if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            #     print(event.data.delta, end="", flush=True)
            # elif event.type == "agent_updated_stream_event":
            #     print(f"Agent updated: {event.new_agent.name}")
            # elif event.type == "run_item_stream_event":
            #     if event.item.type == "tool_call_item":
            #         tool_call = event.item.raw_item
            #         if tool_call.type == 'function_call':
            #             tool_name = tool_call.name
            #             tool_args = tool_call.arguments
            #             print(
            #                 f"\n-- Tool called: {tool_name}, args: {tool_args}")
            #     elif event.item.type == "tool_call_output_item":
            #         print(f"-- Tool output: {event.item.output}")
        print("\n\n=== Run complete ===")

if __name__ == "__main__":
    asyncio.run(main())
