from typing import TypedDict, Optional, Dict, List, Any

from langchain_core.messages import BaseMessage


class AutoMLState(TypedDict):

    """
    Central shared state across the
    Industrial Agentic AutoML workflow.
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
    # TOOL TRACKING
    # =====================================================

    tool_usage_log: Optional[List[str]]

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
    # OBSERVABILITY + TELEMETRY
    # =====================================================

    trace_id: Optional[str]

    workflow_path: Optional[List[str]]

    node_execution_times: Optional[Dict]

    telemetry_data: Optional[Dict]

    trace_file_path: Optional[str]

    replay_available: Optional[bool]

    # =====================================================
    # FEEDBACK + HITL
    # =====================================================

    feedback_score: Optional[int]

    feedback_comment: Optional[str]

    # =====================================================
    # API + STREAMING
    # =====================================================

    api_request_id: Optional[str]

    streaming_status: Optional[str]

    # =====================================================
    # EVALUATION
    # =====================================================

    evaluation_metrics: Optional[Dict[str, Any]]

    hallucination_score: Optional[float]

    relevancy_score: Optional[float]

    tool_accuracy_score: Optional[float]

    evaluation_status: Optional[str]

    evaluation_report_path: Optional[str]

    # =====================================================
    # REPORTING
    # =====================================================

    generated_report: Optional[Dict]