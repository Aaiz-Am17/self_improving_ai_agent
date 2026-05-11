from src.tools.rag_tools import (
    retrieve_ml_knowledge
)


def rag_node(state):

    dataset_summary = state[
        "dataset_summary"
    ]

    query = (
        f"Best preprocessing for dataset: "
        f"{dataset_summary}"
    )

    result = retrieve_ml_knowledge.invoke({
        "query": query
    })

    return {
        "retrieved_knowledge": result,
        "current_agent": "rag_agent"
    }