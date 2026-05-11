def validator_node(state):
    """
    Validator / HITL Agent

    Responsible for:
    - validating preprocessing plan
    - requesting human approval
    - pausing execution before pipeline execution
    """

    preprocessing_plan = state.get(
        "preprocessing_plan",
        {}
    )

    print("\n==============================")
    print("HUMAN APPROVAL REQUIRED")
    print("==============================\n")

    print("PROPOSED PREPROCESSING PLAN:\n")
    print(preprocessing_plan)

    print("\nOPTIONS:")
    print("1 -> approve")
    print("2 -> reject")

    decision = input(
        "\nEnter decision: "
    )

    if decision == "1":

        return {

            "approval_status": "approved",

            "execution_status": "ready_for_execution",

            "current_agent": "validator"
        }

    else:

        return {

            "approval_status": "rejected",

            "execution_status": "stopped",

            "current_agent": "validator"
        }