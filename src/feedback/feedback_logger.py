"""
Feedback logging utilities.
"""

from src.feedback.feedback_database import (
    insert_feedback_log
)


def log_feedback(
    thread_id: str,
    user_input: str,
    agent_response: str,
    feedback_score: int,
    optional_comment: str = ""
):
    """
    Logs user feedback into persistent storage.
    """

    insert_feedback_log(

        thread_id=thread_id,

        user_input=user_input,

        agent_response=agent_response,

        feedback_score=feedback_score,

        optional_comment=optional_comment
    )