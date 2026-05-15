from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):

    thread_id: str

    message: str

    dataset_path: str

    approval_decision: Optional[str] = None


class ChatResponse(BaseModel):

    response: dict