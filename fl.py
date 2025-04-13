import asyncio
from openai.types.responses.response_input_item_param import Message
from agents import Runner
from fl_agents.test_reasoner import test_reasoner_agent
from fl_agents.fault_localizer import fault_localizer_agent
from fl_agents.hooks import fault_localization_run_hook


async def main():
    # result = Runner.run_streamed(
    #     input=[
    #         Message(
    #             role="user",
    #             type="message",
    #             content=[
    #                 {
    #                     'text': 'begin by loading the failing test and reasoning why it fails',
    #                     'type': 'input_text'
    #                 }
    #             ]
    #         )
    #     ],
    #     starting_agent=test_reasoner_agent,
    #     context={
    #         "project_name": "thefuck",
    #         "bug_id": 1,
    #         "failing_test_file": "tests/rules/test_pip_unknown_command.py"
    #     },
    #     hooks=fault_localization_run_hook
    # )

    result = Runner.run_streamed(
        input=[
            Message(
                role="user",
                type="message",
                content=[
                    {
                        'text': """<failing_test_with_reason>
```python
@pytest.mark.parametrize('script, broken, suggested, new_cmd', [
    ('pip un+install thefuck', 'un+install', 'uninstall', 'pip uninstall thefuck'),
])
def test_get_new_command(script, new_cmd, pip_unknown_cmd):
    assert get_new_command(Command(script,
                                  pip_unknown_cmd)) == new_cmd
```

This particular test is causing a failure. Let's break it down:

- **Test Case**: The test case `test_get_new_command` uses a parameterized decorator to test the behavior of the `get_new_command` function with a script that should result in a command suggesting "uninstall".
- **Script** used: `pip un+install thefuck`, which suggests there is an error saying "unknown command 'un+install'".
- **Expected Behavior**: The function `get_new_command` processes this output and tries to extract the broken command part, expecting it to be `'un+install'`.
- **Issue Identified**: During extraction using `re.findall`, the function throws an `IndexError: list index out of range` because the expected "broken" command is not found in the error message. This suggests that the regular expression used to capture the broken command might be incorrectly formulated, leading to it returning an empty list.

The issue here appears to stem from improper handling or extraction logic for parsing a specific format string. The failure happens when trying to grab elements that are not there, indicating either a problem with the test setup or possibly a flaw in the implementation of command processing and error message parsing within `get_new_command`.
</failing_test_with_reason>
                          """,
                        'type': 'input_text'
                    }
                ]
            )
        ],
        starting_agent=fault_localizer_agent,
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
    asyncio.run(main())
