from typing import Dict, Any
from datetime import datetime
import os

from src.evaluation.observability_logger import (
    log_workflow_event
)


REPORT_DIR = "reports"

os.makedirs(REPORT_DIR, exist_ok=True)


def report_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates evaluation reports.
    """

    evaluation_metrics = state.get(
        "evaluation_metrics",
        {}
    )

    timestamp = datetime.utcnow().strftime(
        "%Y%m%d_%H%M%S"
    )

    report_path = os.path.join(

        REPORT_DIR,

        f"evaluation_report_{timestamp}.md"
    )

    report_content = f"""
# Evaluation Report

## Final Scores

- Relevancy Score:
  {evaluation_metrics.get("relevancy_score")}

- Hallucination Score:
  {evaluation_metrics.get("hallucination_score")}

- Tool Accuracy Score:
  {evaluation_metrics.get("tool_accuracy_score")}

- Final Composite Score:
  {evaluation_metrics.get("final_score")}

## Workflow Status

Evaluation completed successfully.
"""

    with open(report_path, "w", encoding="utf-8") as f:

        f.write(report_content)

    # =====================================================
    # OBSERVABILITY LOGGING
    # =====================================================

    log_workflow_event(

        "report_generated",

        {
            "report_path": report_path
        }
    )

    return {

        "evaluation_report_path": report_path
    }