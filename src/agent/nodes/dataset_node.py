from src.tools.dataset_tools import (

    inspect_dataset,

    detect_missing_values,

    analyze_features
)

from src.evaluation.timing_utils import (

    start_timer,

    end_timer
)

from src.observability.telemetry import (

    build_telemetry_payload
)


def dataset_analyst_node(state):

    """
    Dataset Analyst Agent

    Responsible for:
    - dataset inspection
    - missing value analysis
    - feature analysis
    """

    timer = start_timer()

    dataset_path = state["dataset_path"]

    tool_usage_log = state.get(
        "tool_usage_log",
        []
    )

    # =====================================================
    # TOOL EXECUTION
    # =====================================================

    dataset_summary = inspect_dataset.invoke({

        "file_path": dataset_path
    })

    missing_values = detect_missing_values.invoke({

        "file_path": dataset_path
    })

    feature_analysis = analyze_features.invoke({

        "file_path": dataset_path
    })

    # =====================================================
    # TOOL TRACKING
    # =====================================================

    tool_usage_log.extend([

        "inspect_dataset",

        "detect_missing_values",

        "analyze_features"
    ])

    # =====================================================
    # OBSERVABILITY
    # =====================================================

    execution_time = end_timer(timer)

    node_execution_times = state.get(
        "node_execution_times",
        {}
    )

    workflow_path = state.get(
        "workflow_path",
        []
    )

    node_execution_times[
        "dataset_analyst"
    ] = execution_time

    workflow_path.append(
        "dataset_analyst"
    )

    telemetry_payload = build_telemetry_payload(

        thread_id=state.get("thread_id", ""),

        current_agent="dataset_analyst",

        execution_status="completed"
    )

    return {

        "dataset_summary": dataset_summary,

        "missing_values": missing_values,

        "feature_analysis": feature_analysis,

        "tool_usage_log": tool_usage_log,

        "current_agent": "dataset_analyst",

        "node_execution_times": node_execution_times,

        "workflow_path": workflow_path,

        "telemetry_data": telemetry_payload
    }