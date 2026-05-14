"""
Workflow replay utilities.
"""

import json
from pathlib import Path


TRACE_DIR = Path("traces")


def replay_trace(trace_id: str):

    trace_file = TRACE_DIR / f"{trace_id}.json"

    if not trace_file.exists():

        raise FileNotFoundError(
            f"Trace {trace_id} not found."
        )

    with open(trace_file, "r", encoding="utf-8") as f:

        trace_data = json.load(f)

    print("\nWORKFLOW REPLAY:\n")

    print(json.dumps(
        trace_data,
        indent=4
    ))