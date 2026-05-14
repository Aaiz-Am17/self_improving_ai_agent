"""
Observability logging utilities.
"""

from datetime import datetime
from typing import Dict, Any
import json
import os


LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)


def log_workflow_event(
    event_type: str,
    payload: Dict[str, Any]
):
    """
    Logs workflow execution events.
    """

    log_entry = {

        "timestamp": datetime.utcnow().isoformat(),

        "event_type": event_type,

        "payload": payload
    }

    log_file = os.path.join(
        LOG_DIR,
        "workflow_logs.jsonl"
    )

    with open(log_file, "a", encoding="utf-8") as f:

        f.write(json.dumps(log_entry) + "\n")