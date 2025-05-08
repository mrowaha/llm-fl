import sys
import os
import asyncio
import json
from openai.types.responses.response_input_item_param import Message
from agents import Runner, ItemHelpers
from fl_agents.fault_localizer import fault_localizer_agent
from fl_agents.hooks import fault_localization_run_hook
from openai.types.responses import ResponseTextDeltaEvent
from dirs import get_project_bug_dir
from prompts import system_prompt


async def main():
    if len(sys.argv) != 3:
        print('please specify the project name and the bug id')
        os._exit(1)

    project = sys.argv[1]
    bug = int(sys.argv[2])
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

    fl_prompt = f"""
    {failing_test_prompt}

    {executed_lines_prompt}
    """
    result = Runner.run_streamed(
        input=[
            Message(
                role="system",
                type="message",
                content=[
                    {
                        'text': system_prompt,
                        'type': 'input_text'
                    }
                ]
            ),
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
        print("=== Run starting ===")
        print("=== Run staring ===", file=f)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
                print(event.data.delta, end="", file=f)
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    tool_call = event.item.raw_item
                    if tool_call.type == 'function_call':
                        tool_name = tool_call.name
                        tool_args = tool_call.arguments
                        print(f"\n-- Tool was called: {tool_name}")
                        print(f"-- Tool arguments: {tool_args}")
                        print(f"-- Tool was called: {tool_name}", file=f)
                        print(f"-- Tool arguments: {tool_args}", file=f)
                elif event.item.type == "tool_call_output_item":
                    print(f"-- Tool output: {event.item.output}")
                    print(f"-- Tool output: {event.item.output}", file=f)
        print("=== Run complete ===")
        print("=== Run complete ===", file=f)

if __name__ == "__main__":
    asyncio.run(main())
