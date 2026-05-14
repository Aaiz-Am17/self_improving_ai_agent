"""
Session-aware telemetry utilities.
"""

from datetime import datetime


def build_telemetry_payload(
    thread_id: str,
    current_agent: str,
    execution_status: str
):

    return {

        "timestamp": datetime.utcnow().isoformat(),

        "thread_id": thread_id,

        "current_agent": current_agent,

        "execution_status": execution_status
    }