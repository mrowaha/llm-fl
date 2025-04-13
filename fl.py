import asyncio
from openai.types.responses.response_input_item_param import Message
from agents import Runner
from fl_agents.test_reasoner import test_reasoner_agent
from fl_agents.hooks import fault_localization_run_hook


async def main():
    result = Runner.run_streamed(
        input=[
            Message(
                role="user",
                type="message",
                content=[
                    {
                        'text': 'begin by loading the failing test and reasoning why it fails',
                        'type': 'input_text'
                    }
                ]
            )
        ],
        starting_agent=test_reasoner_agent,
        context={
            "project_name": "thefuck",
            "bug_id": 1,
            "failing_test_file": "tests/rules/test_pip_unknown_command.py"
        },
        hooks=fault_localization_run_hook
    )

    async for event in result.stream_events():
        pass
if __name__ == "__main__":
    # llmFl = LLMFl()
    # llmFl_runner = partial(llmFl.run, 1, 'thefuck')
    # asyncio.run(llmFl_runner())
    asyncio.run(main())
