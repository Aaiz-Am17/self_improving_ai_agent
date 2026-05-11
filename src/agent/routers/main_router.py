def main_router(state):
    """
    Main deterministic router.
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

    if state.get("approval_status") == "approved" and \
       not state.get("model_accuracy"):

        return "execution_agent"

    # =====================================================
    # FINISH
    # =====================================================

    return "finish"