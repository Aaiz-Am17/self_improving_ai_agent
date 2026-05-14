from src.tools.rag_tools import (

    retrieve_ml_knowledge
)

from src.evaluation.timing_utils import (

    start_timer,

    end_timer
)

from src.observability.telemetry import (

    build_telemetry_payload
)


def rag_node(state):

    """
    RAG Agent

    Responsible for:
    - retrieving ML best practices
    - enriching pipeline planning
    """

    timer = start_timer()

    dataset_summary = state[
        "dataset_summary"
    ]

    tool_usage_log = state.get(
        "tool_usage_log",
        []
    )

    query = (

        f"Best preprocessing for dataset: "
        f"{dataset_summary}"
    )

    result = retrieve_ml_knowledge.invoke({

        "query": query
    })

    # =====================================================
    # TOOL TRACKING
    # =====================================================

    tool_usage_log.append(
        "retrieve_ml_knowledge"
    )

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
        "rag_agent"
    ] = execution_time

    workflow_path.append(
        "rag_agent"
    )

    telemetry_payload = build_telemetry_payload(

        thread_id=state.get("thread_id", ""),

        current_agent="rag_agent",

        execution_status="completed"
    )

    return {

        "retrieved_knowledge": result,

        "tool_usage_log": tool_usage_log,

        "current_agent": "rag_agent",

        "node_execution_times": node_execution_times,

        "workflow_path": workflow_path,

        "telemetry_data": telemetry_payload
    }