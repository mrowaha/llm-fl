from pathlib import Path


class PromptLoader():
    def __init__(self):
        self.prompts_root_dir = Path("prompts")

    def get_test_reasoning_prompt(self: "PromptLoader", failing_test: str) -> str:
        failing_test_prompt: str
        with open(self.prompts_root_dir / Path("test_reasoning.txt")) as prompt_file:
            failing_test_prompt = prompt_file.read()

        return f"""
      {failing_test_prompt}

      failing_test to examine: {failing_test}
    """
