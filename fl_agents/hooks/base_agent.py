import sys
from agents.lifecycle import AgentHooks
from log import Logger as FlLogger, PrefixedFormatter
from dirs import get_project_bug_dir
project = sys.argv[1]
bug = int(sys.argv[2])

_logger = FlLogger("fl.BaseAgent").configure(
    logging_formatter=PrefixedFormatter(
        '[agent]'
    ),
    file_path=get_project_bug_dir(
        project, bug, 'data') / "fl-agent.log"
).get_logger()


class BaseAgentHooks(AgentHooks):
    async def on_start(self, context, agent):
        _logger.debug(f"agent={agent.name} started")

    async def on_end(self, context, agent, output):
        _logger.debug(f"agent={agent.name} ended with output:\n{output}")

    async def on_tool_start(self, context, agent, tool):
        _logger.debug(f"agent={agent.name} tool start: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        _logger.debug(
            f"agent={agent.name} tool end: {tool.name} with result\n{result}")


base_agent_hook = BaseAgentHooks()
