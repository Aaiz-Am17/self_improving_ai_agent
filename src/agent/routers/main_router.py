def main_router(state):
    """
    Main deterministic router for the
    Industrial Agentic AutoML workflow.
    """

    # =====================================================
    # STEP 1 -> DATASET ANALYSIS
    # =====================================================

    if not state.get("dataset_summary"):

        return "dataset_analyst"

    # =====================================================
    # STEP 2 -> RAG RETRIEVAL
    # =====================================================

    if not state.get("retrieved_knowledge"):

        return "rag_agent"

    # =====================================================
    # STEP 3 -> PIPELINE PLANNING
    # =====================================================

    if not state.get("preprocessing_plan"):

        return "pipeline_architect"

    # =====================================================
    # STEP 4 -> VALIDATION
    # =====================================================

    if not state.get("approval_status"):

        return "validator"

    # =====================================================
    # STEP 5 -> EXECUTION
    # =====================================================

    if (
        state.get("approval_status") == "approved"
        and not state.get("model_accuracy")
    ):

        return "execution_agent"

    # =====================================================
    # STEP 6 -> EVALUATION
    # =====================================================

    if (
        state.get("model_accuracy")
        and not state.get("evaluation_status")
    ):

        return "evaluation_node"

    # =====================================================
    # STEP 7 -> REPORT GENERATION
    # =====================================================

    if (
        state.get("evaluation_status") == "completed"
        and not state.get("evaluation_report_path")
    ):

        return "report_node"

    # =====================================================
    # FINISH
    # =====================================================

    return "finish"