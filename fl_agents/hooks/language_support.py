from agents.lifecycle import AgentHooks
from log import Logger as FlLogger, PrefixedFormatter

_logger = FlLogger("language support agent").configure(
    logging_formatter=PrefixedFormatter(
        '[Agent: Language Support]'
    )
).get_logger()


class LanguageSupportAgentHooks(AgentHooks):
    async def on_start(self, context, agent):
        _logger.debug(f"started: {agent.instructions}")

    async def on_end(self, context, agent, output):
        _logger.debug(f"ended with output:\n{output}")

    async def on_tool_start(self, context, agent, tool):
        _logger.debug(f"tool start: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        _logger.debug(
            f"tool end: {tool.name} with result\n{result}")


language_support_agent_hook = LanguageSupportAgentHooks()
