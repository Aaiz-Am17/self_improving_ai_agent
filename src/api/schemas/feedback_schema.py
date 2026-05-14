from pydantic import BaseModel


class FeedbackRequest(BaseModel):

    thread_id: str

    user_input: str

    agent_response: str

    feedback_score: int

    optional_comment: str = ""