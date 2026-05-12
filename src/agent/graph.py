from langgraph.graph import (
    StateGraph,
    END
)

from src.agent.state import AutoMLState

from src.agent.nodes.dataset_node import (
    dataset_analyst_node
)

from src.agent.nodes.rag_node import (
    rag_node
)

from src.agent.nodes.planner_node import (
    planner_node
)

from src.agent.nodes.validator_node import (
    validator_node
)

from src.agent.nodes.execution_node import (
    execution_node
)

from src.agent.nodes.guardrail_node import (
    guardrail_node
)

from src.agent.nodes.alert_node import (
    alert_node
)

from src.agent.routers.main_router import (
    main_router
)

from src.persistence.checkpointer import (
    checkpointer
)


# =====================================================
# SECURITY ROUTER
# =====================================================

def security_router(state: AutoMLState) -> str:
    """
    Determines whether the request is safe
    enough to continue into the main workflow.
    """

    execution_status = state.get("execution_status", "")

    if execution_status == "BLOCKED":
        return "alert_node"

    return "main_workflow"


# =====================================================
# GRAPH BUILDER
# =====================================================

builder = StateGraph(AutoMLState)


# =====================================================
# ADD SECURITY NODES
# =====================================================

builder.add_node(
    "guardrail_node",
    guardrail_node
)

builder.add_node(
    "alert_node",
    alert_node
)


# =====================================================
# ADD MAIN AGENT NODES
# =====================================================

builder.add_node(
    "dataset_analyst",
    dataset_analyst_node
)

builder.add_node(
    "rag_agent",
    rag_node
)

builder.add_node(
    "pipeline_architect",
    planner_node
)

builder.add_node(
    "validator",
    validator_node
)

builder.add_node(
    "execution_agent",
    execution_node
)


# =====================================================
# GRAPH ENTRY POINT
# =====================================================

builder.set_entry_point("guardrail_node")


# =====================================================
# SECURITY ROUTING
# =====================================================

builder.add_conditional_edges(

    "guardrail_node",

    security_router,

    {
        "alert_node": "alert_node",
        "main_workflow": "dataset_analyst"
    }
)


# =====================================================
# ALERT NODE ENDS EXECUTION
# =====================================================

builder.add_edge(
    "alert_node",
    END
)


# =====================================================
# CONDITIONAL EDGES
# =====================================================

builder.add_conditional_edges(

    "dataset_analyst",

    main_router,

    {
        "dataset_analyst": "dataset_analyst",

        "rag_agent": "rag_agent",

        "pipeline_architect": "pipeline_architect",

        "validator": "validator",

        "execution_agent": "execution_agent",

        "finish": END
    }
)


builder.add_conditional_edges(

    "rag_agent",

    main_router,

    {
        "dataset_analyst": "dataset_analyst",

        "rag_agent": "rag_agent",

        "pipeline_architect": "pipeline_architect",

        "validator": "validator",

        "execution_agent": "execution_agent",

        "finish": END
    }
)


builder.add_conditional_edges(

    "pipeline_architect",

    main_router,

    {
        "dataset_analyst": "dataset_analyst",

        "rag_agent": "rag_agent",

        "pipeline_architect": "pipeline_architect",

        "validator": "validator",

        "execution_agent": "execution_agent",

        "finish": END
    }
)


builder.add_conditional_edges(

    "validator",

    main_router,

    {
        "dataset_analyst": "dataset_analyst",

        "rag_agent": "rag_agent",

        "pipeline_architect": "pipeline_architect",

        "validator": "validator",

        "execution_agent": "execution_agent",

        "finish": END
    }
)


builder.add_conditional_edges(

    "execution_agent",

    main_router,

    {
        "dataset_analyst": "dataset_analyst",

        "rag_agent": "rag_agent",

        "pipeline_architect": "pipeline_architect",

        "validator": "validator",

        "execution_agent": "execution_agent",

        "finish": END
    }
)


# =====================================================
# COMPILE GRAPH
# =====================================================

graph = builder.compile(
    checkpointer=checkpointer
)