import os
from langgraph.graph import StateGraph, START, END
from app.agent.schemas import AgentState, AgentAction
from langchain_core.messages import SystemMessage, HumanMessage
import json

# Setup Gemini LLM using langchain-google-genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

def call_model(state: dict):
    # This node analyzes the context and produces an action
    llm_provider = os.environ.get("LLM_PROVIDER", "gemini").lower()
    
    if llm_provider == "ollama":
        ollama_model = os.environ.get("OLLAMA_MODEL", "llama3")
        llm = ChatOllama(model=ollama_model, base_url="http://localhost:11434")
    else:
        from app.core.config import get_settings
        settings = get_settings()
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return {
                "proposed_action": AgentAction(
                    action_type="escalate",
                    payload={"reason": "Missing API Key"},
                    rationale_text="Escalating to human due to missing GEMINI_API_KEY"
                )
            }
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)
        
    structured_llm = llm.with_structured_output(AgentAction)
    
    sys_msg = state.get("system_prompt", "You are an AI recovery agent.")
    sys_msg += f"\nContext: {json.dumps(state.get('context', {}))}"
    
    try:
        result = structured_llm.invoke([
            SystemMessage(content=sys_msg),
            HumanMessage(content="Determine the best recovery action.")
        ])
        return {"proposed_action": result}
    except Exception as e:
        # Fallback to escalate on any LLM failure
        return {
            "proposed_action": AgentAction(
                action_type="escalate",
                payload={"error": str(e)},
                rationale_text=f"LLM API failed. Automatically escalating to a human. Error: {str(e)}"
            )
        }

def build_graph():
    builder = StateGraph(dict) # Simplified state typed as dict for compatibility
    
    builder.add_node("analyze", call_model)
    builder.add_edge(START, "analyze")
    builder.add_edge("analyze", END)
    
    return builder.compile()
