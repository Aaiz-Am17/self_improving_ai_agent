from typing import Dict, Any
from datetime import datetime
import os
import json

from src.evaluation.observability_logger import (
    log_workflow_event
)

from src.config.paths import (
    REPORTS_DIR
)


# =====================================================
# ENSURE REPORT DIRECTORY EXISTS
# =====================================================

os.makedirs(
    REPORTS_DIR,
    exist_ok=True
)


def report_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates:
    - Markdown evaluation report
    - JSON telemetry report
    - Workflow observability summary
    """

    evaluation_metrics = state.get(
        "evaluation_metrics",
        {}
    )

    workflow_path = state.get(
        "workflow_path",
        []
    )

    node_execution_times = state.get(
        "node_execution_times",
        {}
    )

    telemetry_data = state.get(
        "telemetry_data",
        {}
    )

    model_accuracy = state.get(
        "model_accuracy"
    )

    timestamp = datetime.utcnow().strftime(
        "%Y%m%d_%H%M%S"
    )

    # =====================================================
    # REPORT PATHS
    # =====================================================

    markdown_report_path = os.path.join(

        REPORTS_DIR,

        f"evaluation_report_{timestamp}.md"
    )

    json_report_path = os.path.join(

        REPORTS_DIR,

        f"evaluation_report_{timestamp}.json"
    )

    # =====================================================
    # MARKDOWN REPORT CONTENT
    # =====================================================

    report_content = f"""
# Industrial Agentic AutoML Evaluation Report

Generated At:
{datetime.utcnow().isoformat()} UTC

---

# MODEL PERFORMANCE

- Model Accuracy:
  {model_accuracy}

---

# EVALUATION METRICS

- Relevancy Score:
  {evaluation_metrics.get("relevancy_score")}

- Hallucination Score:
  {evaluation_metrics.get("hallucination_score")}

- Tool Accuracy Score:
  {evaluation_metrics.get("tool_accuracy_score")}

- Final Composite Score:
  {evaluation_metrics.get("final_score")}

- Passed Thresholds:
  {evaluation_metrics.get("passed_thresholds")}

---

# WORKFLOW PATH

{workflow_path}

---

# NODE EXECUTION TIMES

{node_execution_times}

---

# TELEMETRY

{telemetry_data}

---

# FINAL STATUS

Evaluation completed successfully.
"""

    # =====================================================
    # SAVE MARKDOWN REPORT
    # =====================================================

    with open(
        markdown_report_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report_content)

    # =====================================================
    # JSON REPORT
    # =====================================================

    json_payload = {

        "timestamp": timestamp,

        "model_accuracy": model_accuracy,

        "evaluation_metrics": evaluation_metrics,

        "workflow_path": workflow_path,

        "node_execution_times": node_execution_times,

        "telemetry_data": telemetry_data
    }

    with open(
        json_report_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            json_payload,
            f,
            indent=4
        )

    # =====================================================
    # OBSERVABILITY LOGGING
    # =====================================================

    log_workflow_event(

        "report_generated",

        {

            "markdown_report": markdown_report_path,

            "json_report": json_report_path
        }
    )

    return {

        "evaluation_report_path": markdown_report_path,

        "execution_status": "completed",

        "current_agent": "report_node"
    }