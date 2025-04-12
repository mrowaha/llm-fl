import logging
from log import Logger, PrefixedFormatter
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from typing import Optional
test_reasoner_model_id = 'deepseek-r1:8b'

test_reasoner_model = OpenAIChatCompletionsModel(
    model=test_reasoner_model_id,
    openai_client=AsyncOpenAI(
        base_url="http://localhost:11434/v1", api_key="ollama")
)


class TestReasonerAgent():

    _instance: Optional["TestReasonerAgent"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TestReasonerAgent, cls).__new__(cls)
            cls._instance.__initialize_agent()
        return cls._instance

    def __initialize_agent(self: "TestReasonerAgent") -> None:
        self.__logger = Logger("test_reasoner").configure(
            level=logging.DEBUG,
            logging_formatter=PrefixedFormatter("[TEST REASONER]")).get_logger()
        self.__agent = Agent(
            name="Test Reasoning Agent",
            instructions="",
            model=test_reasoner_model
        )

    async def stream_response(self, reasoner_query: str, *, bug_id: int, project: str):
        self.__logger.info(
            f"generating test reasoning response for {project}:{bug_id}")
        result = Runner.run_streamed(
            self.__agent,
            reasoner_query
        )

        async for event in result.stream_events():
            if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta
                yield delta
