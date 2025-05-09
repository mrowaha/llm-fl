import sys
import logging
from datetime import datetime, timezone
from agents.lifecycle import AgentHooks
from log import Logger as FlLogger, PrefixedFormatter
from dirs import get_project_bug_dir
project = sys.argv[1]
bug = int(sys.argv[2])


class BaseAgentHooks(AgentHooks):

    def set_logger(self, logger: logging.Logger):
        self._logger = logger

    async def on_start(self, context, agent):
        self._logger.debug(f"agent={agent.name} started")

    async def on_end(self, context, agent, output):
        self._logger.debug(f"agent={agent.name} ended with output:\n{output}")

    async def on_tool_start(self, context, agent, tool):
        self._logger.debug(f"agent={agent.name} tool start: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        self._logger.debug(
            f"agent={agent.name} tool end: {tool.name} with result\n{result}")


def get_fault_localizer_hooks() -> BaseAgentHooks:
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%MZ')
    base_agent_hook = BaseAgentHooks()
    _logger = FlLogger("fl.FaultLocalizerAgent").configure(
        stdout=False,
        logging_formatter=PrefixedFormatter(
            '\n[agent]'
        ),
        file_path=get_project_bug_dir(
            project, bug, 'data') / f"fl-agent-{now}.log"
    ).get_logger()

    base_agent_hook.set_logger(_logger)
    return base_agent_hook


def get_coverage_analyzer_hooks() -> BaseAgentHooks:
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%MZ')
    base_agent_hook = BaseAgentHooks()
    _logger = FlLogger("fl.CoverageAnalyzerAgent").configure(
        stdout=False,
        logging_formatter=PrefixedFormatter(
            '\n[agent]'
        ),
        file_path=get_project_bug_dir(
            project, bug, 'data') / f"ca-agent-{now}.log"
    ).get_logger()
    base_agent_hook.set_logger(_logger)
    return base_agent_hook
