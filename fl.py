from pathlib import Path
from prompt_loader import PromptLoader
from fl_agents import TestReasonerAgent
import asyncio
from functools import partial
from key_store import s, static_keys
from dirs import get_project_bug_dir


class LLMFl():
    def __init__(self):
        self.prompt_loader = PromptLoader()
        self.test_reasoner_agent = TestReasonerAgent()

    async def reason_failing_test(self: "LLMFl", bug_id: int, project_name: str) -> None:
        failing_test: str
        with open(get_project_bug_dir(project_name, bug_id, 'data') / Path("failing_test.txt")) as failing_test_file:
            failing_test = failing_test_file.read()
        test_reasoning_prompt = self.prompt_loader.get_test_reasoning_prompt(
            failing_test)

        with open(get_project_bug_dir(project_name, bug_id, 'preprocessed') / Path("test_reasoning.txt"), "wb") as processed_file:
            async for response_delta in self.test_reasoner_agent.stream_response(
                test_reasoning_prompt,
                bug_id=bug_id,
                project=project_name
            ):
                processed_file.write(response_delta.encode(errors='ignore'))
                processed_file.flush()

        with open(get_project_bug_dir(project_name, bug_id, 'preprocessed') / Path("test_reasoning.txt"), "rb") as processed_file:
            s.set(static_keys['test_reason'],
                  processed_file.read())

        print(bytes(s.get(static_keys['test_reason'])).decode(errors='ignore'))

    async def run(self, bug_id: int, project_name: str) -> None:
        await self.reason_failing_test(bug_id, project_name)


if __name__ == "__main__":
    llmFl = LLMFl()
    llmFl_runner = partial(llmFl.run, 1, 'thefuck')
    asyncio.run(llmFl_runner())
