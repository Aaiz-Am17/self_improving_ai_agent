from typing import Dict, Any

from src.evaluation.evaluation_metrics import (

    keyword_relevancy_score
)

from src.evaluation.hallucination_detector import (

    detect_hallucinations
)

from src.evaluation.tool_accuracy import (

    evaluate_tool_usage
)

from src.evaluation.observability_logger import (

    log_workflow_event
)

from src.evaluation.thresholds import (

    MIN_FINAL_SCORE,

    MIN_HALLUCINATION_SCORE,

    MIN_RELEVANCY_SCORE,

    MIN_TOOL_ACCURACY
)

from src.evaluation.timing_utils import (

    start_timer,

    end_timer
)

from src.observability.telemetry import (

    build_telemetry_payload
)


def evaluation_node(state: Dict[str, Any]) -> Dict[str, Any]:

    """
    Advanced workflow evaluation node.
    """

    timer = start_timer()

    response = str(
        state.get("pipeline_output", "")
    )

    tool_usage_log = state.get(
        "tool_usage_log",
        []
    )

    workflow_path = state.get(
        "workflow_path",
        []
    )

    node_execution_times = state.get(
        "node_execution_times",
        {}
    )

    # =====================================================
    # EXPECTED TARGETS
    # =====================================================

    expected_keywords = [

        "missing",

        "encoding",

        "scaling",

        "preprocessing"
    ]

    expected_tools = [

        "inspect_dataset",

        "detect_missing_values",

        "analyze_features",

        "retrieve_ml_knowledge"
    ]

    # =====================================================
    # SCORING
    # =====================================================

    relevancy = keyword_relevancy_score(

        response,

        expected_keywords
    )

    hallucination = detect_hallucinations(
        response
    )

    tool_accuracy = evaluate_tool_usage(

        tool_usage_log,

        expected_tools
    )

    final_score = round(

        (
            relevancy +
            hallucination +
            tool_accuracy
        ) / 3,

        3
    )

    # =====================================================
    # THRESHOLD GATING
    # =====================================================

    passed = (

        relevancy >= MIN_RELEVANCY_SCORE
        and hallucination >= MIN_HALLUCINATION_SCORE
        and tool_accuracy >= MIN_TOOL_ACCURACY
        and final_score >= MIN_FINAL_SCORE
    )

    evaluation_metrics = {

        "relevancy_score": relevancy,

        "hallucination_score": hallucination,

        "tool_accuracy_score": tool_accuracy,

        "final_score": final_score,

        "passed_thresholds": passed
    }

    # =====================================================
    # OBSERVABILITY
    # =====================================================

    evaluation_time = end_timer(timer)

    node_execution_times[
        "evaluation_node"
    ] = evaluation_time

    workflow_path.append(
        "evaluation_node"
    )

    telemetry_payload = build_telemetry_payload(

        thread_id=state.get("thread_id", ""),

        current_agent="evaluation_node",

        execution_status="completed"
    )

    # =====================================================
    # LOGGING
    # =====================================================

    log_workflow_event(

        "evaluation_completed",

        {

            "metrics": evaluation_metrics,

            "evaluation_time": evaluation_time
        }
    )

    return {

        "evaluation_metrics": evaluation_metrics,

        "hallucination_score": hallucination,

        "relevancy_score": relevancy,

        "tool_accuracy_score": tool_accuracy,

        "evaluation_status": "completed",

        "node_execution_times": node_execution_times,

        "workflow_path": workflow_path,

        "telemetry_data": telemetry_payload
    }