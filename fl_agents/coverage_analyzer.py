from agents import Agent
from fl_agents.hooks.base_agent import base_agent_hook
# from models import deepseek_chat_model as coverage_analyzer_model
# from models import qwen_code_model as fault_localizer_model
from models import qwen_base_model as coverage_analyzer_model
# from models import deepseek_r1_model as coverage_analyzer_model
from prompts import analyze_coverage_prompt, system_prompt_editor

coverage_analyzer_agent = Agent(
    model=coverage_analyzer_model,
    name="Coverage Analyzer Agent",
    instructions=f"""
    {analyze_coverage_prompt}
    """.strip(),
    hooks=base_agent_hook
)
