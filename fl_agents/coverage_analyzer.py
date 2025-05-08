from agents import Agent
from fl_agents.hooks.base_agent import get_coverage_analyzer_hooks
from models import deepseek_chat_model as coverage_analyzer_model
# from models import qwen_base_model as coverage_analyzer_model
# from models import deepseek_r1_model as coverage_analyzer_model
from prompts import analyze_coverage_prompt, keep_definitions_prompt

coverage_analyzer_agent = Agent(
    model=coverage_analyzer_model,
    name="Coverage Analyzer Agent",
    instructions=f"""
    <your role>
    {keep_definitions_prompt}
    </your role>
    """.strip(),
    hooks=get_coverage_analyzer_hooks()
)
