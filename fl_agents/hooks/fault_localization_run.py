from agents.lifecycle import RunHooks
from log import Logger as FlLogger, PrefixedFormatter
_logger = FlLogger("fault localization run").configure(
    logging_formatter=PrefixedFormatter(
        '[Runner: Fault Localization]'
    )).get_logger()


class FaultLocalizationRunHook(RunHooks):

    async def on_agent_start(self, context, agent):
        _logger.debug(f"the agent {agent.name} has started")
        _logger.debug(f"agent started with context: {context.context}")

    async def on_handoff(self, context, from_agent, to_agent):
        _logger.debug(f"handoff: {from_agent.name} to {to_agent.name}")
        _logger.debug(f"agentic handoff with context: {context.context}")

    async def on_agent_end(self, context, agent, output):
        _logger.debug(f"agent {agent.name} has ended")


fault_localization_run_hook = FaultLocalizationRunHook()
