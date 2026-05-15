from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    thread_id: str
    dataset_path: str
    # Make these optional so the HITL buttons don't crash the API
    message: Optional[str] = None
    approval_decision: Optional[str] = None 

class ChatResponse(BaseModel):
    response: dict
    needs_approval: Optional[bool] = False