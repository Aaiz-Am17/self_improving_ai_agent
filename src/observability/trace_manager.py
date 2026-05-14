"""
Trace management system.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path


TRACE_DIR = Path("traces")

TRACE_DIR.mkdir(exist_ok=True)


def create_trace_id() -> str:

    return str(uuid.uuid4())


def save_workflow_trace(
    trace_id: str,
    workflow_data: dict
):
    """
    Saves workflow execution traces.
    """

    trace_file = TRACE_DIR / f"{trace_id}.json"

    trace_payload = {

        "timestamp": datetime.utcnow().isoformat(),

        "trace_id": trace_id,

        "workflow_data": workflow_data
    }

    with open(trace_file, "w", encoding="utf-8") as f:

        json.dump(
            trace_payload,
            f,
            indent=4
        )