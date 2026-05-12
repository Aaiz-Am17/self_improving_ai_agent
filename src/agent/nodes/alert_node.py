# src/agent/nodes/alert_node.py

from typing import Dict, Any

from langchain_core.messages import AIMessage


def alert_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns a standardized refusal response
    for unsafe or malicious requests.
    """

    security_flags = state.get("security_flags", [])

    refusal_message = (
        "Request blocked by security guardrails.\n\n"
        f"Detected Issues:\n- " + "\n- ".join(security_flags)
    )

    return {
        "messages": [
            AIMessage(content=refusal_message)
        ],
        "execution_status": "BLOCKED"
    }