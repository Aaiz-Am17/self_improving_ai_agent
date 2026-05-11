from typing import TypedDict, Optional, Dict, List
from langchain_core.messages import BaseMessage


class AutoMLState(TypedDict):
    """
    Central shared state across the LangGraph workflow.
    """

    # =====================================================
    # CONVERSATION HISTORY
    # =====================================================

    messages: List[BaseMessage]

    # =====================================================
    # DATASET INFORMATION
    # =====================================================

    dataset_path: Optional[str]

    dataset_summary: Optional[Dict]

    missing_values: Optional[Dict]

    feature_analysis: Optional[Dict]

    # =====================================================
    # RAG RETRIEVALS
    # =====================================================

    retrieved_knowledge: Optional[List[Dict]]

    # =====================================================
    # PIPELINE PLANNING
    # =====================================================

    preprocessing_plan: Optional[Dict]

    pipeline_output: Optional[Dict]

    # =====================================================
    # HUMAN FEEDBACK / HITL
    # =====================================================

    human_feedback: Optional[Dict]

    approval_status: Optional[str]

    # =====================================================
    # EXECUTION RESULTS
    # =====================================================

    model_accuracy: Optional[float]

    trained_model_path: Optional[str]

    # =====================================================
    # RUNTIME TRACKING
    # =====================================================

    execution_status: Optional[str]

    current_agent: Optional[str]

    next_step: Optional[str]

    # =====================================================
    # PERSISTENCE
    # =====================================================

    thread_id: str

    # =====================================================
    # SECURITY
    # =====================================================

    guardrail_status: Optional[str]

    # =====================================================
    # OBSERVABILITY
    # =====================================================

    trace_id: Optional[str]