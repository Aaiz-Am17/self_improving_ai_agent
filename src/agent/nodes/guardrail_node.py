# src/agent/nodes/guardrail_node.py

from typing import Dict, Any

from src.security.validators import validate_user_input


def guardrail_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Security guardrail node.

    Validates user input before allowing the request
    to enter the main agent workflow.
    """

    messages = state.get("messages", [])

    if not messages:
        return {
            "security_flags": ["No messages found."]
        }

    latest_message = messages[-1]

    user_input = str(latest_message.content)

    validation_result = validate_user_input(user_input)

    if validation_result.is_safe:

        return {
            "security_flags": [],
            "execution_status": "SAFE"
        }

    return {
        "security_flags": validation_result.detected_issues,
        "execution_status": "BLOCKED"
    }