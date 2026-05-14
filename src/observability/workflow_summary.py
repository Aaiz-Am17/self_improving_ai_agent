def summarize_workflow(state):

    """
    Generates readable workflow summary.
    """

    print("\n==============================")
    print("WORKFLOW SUMMARY")
    print("==============================\n")

    print("Workflow Path:")
    print(state.get("workflow_path"))

    print("\nExecution Times:")
    print(state.get("node_execution_times"))

    print("\nModel Accuracy:")
    print(state.get("model_accuracy"))

    print("\nEvaluation Metrics:")
    print(state.get("evaluation_metrics"))