from src.evaluation.timing_utils import (

    start_timer,

    end_timer
)

from src.observability.telemetry import (

    build_telemetry_payload
)


def planner_node(state):

    """
    Pipeline Architect Agent

    Responsible for:
    - preprocessing planning
    - encoding decisions
    - scaling decisions
    - missing value strategies
    """

    timer = start_timer()

    feature_analysis = state.get(
        "feature_analysis",
        {}
    )

    missing_values = state.get(
        "missing_values",
        {}
    )

    tool_usage_log = state.get(
        "tool_usage_log",
        []
    )

    # =====================================================
    # EXTRACT INFORMATION
    # =====================================================

    numeric_columns = feature_analysis.get(
        "numeric_columns",
        []
    )

    categorical_columns = feature_analysis.get(
        "categorical_columns",
        []
    )

    low_cardinality = feature_analysis.get(
        "low_cardinality_columns",
        []
    )

    high_cardinality = feature_analysis.get(
        "high_cardinality_columns",
        []
    )

    missing_dict = missing_values.get(
        "missing_values",
        {}
    )

    # =====================================================
    # BUILD STRUCTURED PLAN
    # =====================================================

    preprocessing_plan = {

        "missing_value_strategy": {

            "numeric_columns": {

                "strategy": "median_imputation",

                "columns": [

                    col

                    for col in numeric_columns

                    if missing_dict.get(col, 0) > 0
                ]
            },

            "categorical_columns": {

                "strategy": "most_frequent",

                "columns": [

                    col

                    for col in categorical_columns

                    if missing_dict.get(col, 0) > 0
                ]
            }
        },

        "encoding_strategy": {

            "one_hot_encoding": low_cardinality,

            "target_encoding": high_cardinality
        },

        "scaling_strategy": {

            "method": "StandardScaler",

            "columns": numeric_columns
        }
    }

    # =====================================================
    # TOOL TRACKING
    # =====================================================

    tool_usage_log.extend([

        "median_imputation",

        "one_hot_encoding",

        "StandardScaler"
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
        "pipeline_architect"
    ] = execution_time

    workflow_path.append(
        "pipeline_architect"
    )

    telemetry_payload = build_telemetry_payload(

        thread_id=state.get("thread_id", ""),

        current_agent="pipeline_architect",

        execution_status="completed"
    )

    return {

        "preprocessing_plan": preprocessing_plan,

        "tool_usage_log": tool_usage_log,

        "current_agent": "pipeline_architect",

        "node_execution_times": node_execution_times,

        "workflow_path": workflow_path,

        "telemetry_data": telemetry_payload
    }