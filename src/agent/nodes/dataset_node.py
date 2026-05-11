from src.tools.dataset_tools import (
    inspect_dataset,
    detect_missing_values,
    analyze_features
)


def dataset_analyst_node(state):
    """
    Dataset Analyst Agent

    Responsible for:
    - dataset inspection
    - missing value analysis
    - feature analysis
    """

    dataset_path = state["dataset_path"]

    dataset_summary = inspect_dataset.invoke({
        "file_path": dataset_path
    })

    missing_values = detect_missing_values.invoke({
        "file_path": dataset_path
    })

    feature_analysis = analyze_features.invoke({
        "file_path": dataset_path
    })

    return {
        "dataset_summary": dataset_summary,
        "missing_values": missing_values,
        "feature_analysis": feature_analysis
    }