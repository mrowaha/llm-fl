from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.tool import FunctionTool
from agents.run_context import RunContextWrapper
from openai.types.responses import ResponseTextDeltaEvent
from lang.language_support import get_function_body, get_executed_function_body
from log import Logger, PrefixedFormatter
from typing import Optional, List
import json
language_support_model_id = 'qwen2.5:7b-instruct-8k'

language_support_model = OpenAIChatCompletionsModel(
    model=language_support_model_id,
    openai_client=AsyncOpenAI(
        base_url="http://localhost:11434/v1", api_key="ollama")
)


async def get_function_body_tool(run_context: RunContextWrapper, str_args) -> str:
    args = json.loads(str_args)
    print(args)
    function_body = get_function_body(
        run_context.context['project_name'],
        int(run_context.context['bug_id']),
        args['file_path'],
        args['function_name']
    )

    executed_function_body = get_executed_function_body(
        run_context.context['project_name'],
        int(run_context.context['bug_id']),
        args['file_path'],
        args['function_name']
    )
    print(executed_function_body)
    return function_body

language_support_tools: List[FunctionTool] = [
    FunctionTool(
        name="get_function_body_tool",
        description="returns a function body for a given function name and file path",
        params_json_schema={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path in which the function is housed in"
                },
                "function_name": {
                    "type": "string",
                    "description": "the name of the function that we need the function body for"
                }
            }
        },
        on_invoke_tool=get_function_body_tool
    )
]


class LanguageSupportAgent():

    _instance: Optional["LanguageSupportAgent"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageSupportAgent, cls).__new__(cls)
            cls._instance.__initialize_agent()
        return cls._instance

    def __initialize_agent(self: "LanguageSupportAgent") -> None:
        self.__logger = Logger("language_support_agent").configure(
            logging_formatter=PrefixedFormatter("[LANGUAGE SUPPORT AGENT]")
        ).get_logger()

        self.__agent = Agent(
            name="Language Support Agent",
            tools=language_support_tools,
            model=language_support_model
        )

    async def get_support(
        self: "LanguageSupportAgent",
        project_name: str,
        bug_id: int,
        support_prompt: str
    ):
        result = Runner.run_streamed(
            self.__agent,
            support_prompt,
            context={
                "project_name": project_name,
                "bug_id": bug_id
            }
        )

        async for event in result.stream_events():
            if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                print(event)
                delta = event.data.delta
                yield delta
