import sys
import os

if len(sys.argv) != 3:
    print('please specify the project name and the bug id')
    os._exit(1)

import asyncio
import json
from openai.types.responses.response_input_item_param import Message
from agents import Runner, ItemHelpers
from fl_agents.coverage_analyzer import coverage_analyzer_agent
from openai.types.responses import ResponseTextDeltaEvent
from dirs import get_project_bug_dir
from prompts import system_prompt_editor
from log import Logger as RunLogger, NoNewlineFormatter
from dirs import get_minified_annotations_folder

project = sys.argv[1]
bug = int(sys.argv[2])
_logger = RunLogger("fl.Run").configure(
    logging_formatter=NoNewlineFormatter()
).get_logger()


async def main():
    global project, bug

    file = 'thefuck/utils.py'
    minified_annotations_dir = get_minified_annotations_folder(
        project, bug)

    file_content: str = ""
    with open(
        os.path.join(str(minified_annotations_dir), file+',cover')
    ) as f:
        file_content = f.read()

    file_content = f"""
    <file_executed_content file={file}>
    {file_content}
    </file_executed_content>
    """

    file_content_prompt = f"""
    here is the following file, that you should examine and shorten based on the rules
    {file_content}
    """

    result = Runner.run_streamed(
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

    with open(get_project_bug_dir(project, bug, 'data') / 'fl-run.txt', 'w') as f:
        print("=== Run starting ===\n\n")
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
            elif event.type == "agent_updated_stream_event":
                print(f"Agent updated: {event.new_agent.name}")
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    tool_call = event.item.raw_item
                    if tool_call.type == 'function_call':
                        tool_name = tool_call.name
                        tool_args = tool_call.arguments
                        print(
                            f"\n-- Tool called: {tool_name}, args: {tool_args}")
                elif event.item.type == "tool_call_output_item":
                    print(f"-- Tool output: {event.item.output}")
        print("\n\n=== Run complete ===")

if __name__ == "__main__":
    asyncio.run(main())
