from pydantic import BaseModel


class ChatRequest(BaseModel):

    thread_id: str

    message: str

    dataset_path: str


class ChatResponse(BaseModel):

    response: dict