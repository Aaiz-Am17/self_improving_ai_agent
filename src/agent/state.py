from typing import TypedDict, Optional, Dict, List, Any
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

    security_flags: Optional[List[str]]

    # =====================================================
    # OBSERVABILITY
    # =====================================================

    trace_id: Optional[str]

    node_execution_times: Optional[Dict[str, float]]

    tool_usage_log: Optional[List[str]]

    workflow_path: Optional[List[str]]

    # =====================================================
    # EVALUATION
    # =====================================================

    evaluation_metrics: Optional[Dict[str, Any]]

    hallucination_score: Optional[float]

    relevancy_score: Optional[float]

    tool_accuracy_score: Optional[float]

    evaluation_status: Optional[str]

    evaluation_report_path: Optional[str]