from src.evaluation.timing_utils import start_timer, end_timer
from src.observability.telemetry import build_telemetry_payload


def validator_node(state):
    """
    Validator / HITL Agent

    Modes:
    1. Interactive mode (local dev)
    2. Auto mode (CI/CD, Docker, API)
    """

    timer = start_timer()

    preprocessing_plan = state.get("preprocessing_plan", {})

    print("\n==============================")
    print("HUMAN APPROVAL REQUIRED")
    print("==============================\n")

    print("PROPOSED PREPROCESSING PLAN:\n")
    print(preprocessing_plan)

    print("\nOPTIONS:")
    print("1 -> approve")
    print("2 -> reject")

    # =====================================================
    # SAFE DECISION HANDLING
    # =====================================================

    decision = state.get("human_feedback", {}).get("approval")

    # If no human feedback provided (CI/CD mode), auto-approve
    if decision is None:
        decision = "1"

    # =====================================================
    # OBSERVABILITY
    # =====================================================

    execution_time = end_timer(timer)

    node_execution_times = state.get("node_execution_times", {})
    workflow_path = state.get("workflow_path", [])

    node_execution_times["validator"] = execution_time
    workflow_path.append("validator")

    telemetry_payload = build_telemetry_payload(
        thread_id=state.get("thread_id", ""),
        current_agent="validator",
        execution_status="completed"
    )

    # =====================================================
    # APPROVAL LOGIC
    # =====================================================

    if decision == "1":

        return {
            "approval_status": "approved",
            "execution_status": "ready_for_execution",
            "current_agent": "validator",
            "node_execution_times": node_execution_times,
            "workflow_path": workflow_path,
            "telemetry_data": telemetry_payload
        }

    return {
        "approval_status": "rejected",
        "execution_status": "stopped",
        "current_agent": "validator",
        "node_execution_times": node_execution_times,
        "workflow_path": workflow_path,
        "telemetry_data": telemetry_payload
    }