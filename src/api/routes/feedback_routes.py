from fastapi import APIRouter

from src.api.schemas.feedback_schema import (
    FeedbackRequest
)

from src.feedback.feedback_logger import (
    log_feedback
)

router = APIRouter()


@router.post("/feedback")
def feedback_endpoint(
    request: FeedbackRequest
):

    log_feedback(

        thread_id=request.thread_id,

        user_input=request.user_input,

        agent_response=request.agent_response,

        feedback_score=request.feedback_score,

        optional_comment=request.optional_comment
    )

    return {

        "status": "feedback logged"
    }