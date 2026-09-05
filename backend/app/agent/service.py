from typing import Dict, Any
from app.recovery.schemas import ActionProposal
from app.agent.graph import build_graph
from app.agent.strategy_factory import StrategyFactory
import uuid

class AgentService:
    def __init__(self):
        self.graph = build_graph()

    async def run(self, scenario_type: str, context: Dict[str, Any]) -> ActionProposal:
        strategy = StrategyFactory.get(scenario_type)
        
        rich_context = await strategy.collect_context(context)
        system_prompt = strategy.get_system_prompt()
        
        # Prepare the state for LangGraph
        initial_state = {
            "scenario_type": scenario_type,
            "context": rich_context,
            "system_prompt": system_prompt
        }
        
        # We need an async config with a thread_id if we want checkpointer memory later
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        
        # Execute the graph
        final_state = await self.graph.ainvoke(initial_state, config=config)
        
        # Extract the structured response
        agent_action = final_state.get("proposed_action")
        
        # Map AgentAction to ActionProposal for the orchestrator
        return ActionProposal(
            case_id=context.get("case_id", "unknown"),
            action_type=agent_action.action_type if agent_action else "escalate",
            payload=agent_action.payload if agent_action else {"reason": "Fallback"},
            rationale_text=agent_action.rationale_text if agent_action else "LLM failed to produce a valid action"
        )
