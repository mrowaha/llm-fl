from agents.lifecycle import AgentHooks
from log import Logger as FlLogger, PrefixedFormatter

_logger = FlLogger("test reasoner agent").configure(
    logging_formatter=PrefixedFormatter(
        '[Agent: Test Reasoner]'
    )
).get_logger()


class TestReasonerAgentHooks(AgentHooks):
    async def on_start(self, context, agent):
        _logger.debug("started")

    async def on_end(self, context, agent, output):
        _logger.debug(f"ended with output:\n{output}")
        context.context['failing_reason'] = output

    async def on_tool_start(self, context, agent, tool):
        _logger.debug(f"tool start: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        _logger.debug(
            f"tool end: {tool.name} with result\n{result}")


test_reasoner_agent_hook = TestReasonerAgentHooks()
