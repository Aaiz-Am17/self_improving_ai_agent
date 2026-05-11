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

from src.agent.routers.main_router import (
    main_router
)

from src.persistence.checkpointer import (
    checkpointer
)


# =====================================================
# GRAPH BUILDER
# =====================================================

builder = StateGraph(AutoMLState)


# =====================================================
# ADD NODES
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
# CONDITIONAL ENTRY POINT
# =====================================================

builder.set_conditional_entry_point(

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