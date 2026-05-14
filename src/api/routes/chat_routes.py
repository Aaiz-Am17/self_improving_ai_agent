from fastapi import APIRouter

from langchain_core.messages import HumanMessage

from src.agent.graph import graph

from src.api.schemas.chat_schema import (
    ChatRequest
)

router = APIRouter()


@router.post("/chat")
def chat_endpoint(request: ChatRequest):

    initial_state = {

        "messages": [

            HumanMessage(
                content=request.message
            )
        ],

        "dataset_path": request.dataset_path,

        "thread_id": request.thread_id
    }

    result = graph.invoke(
        initial_state
    )

    return {

        "response": result
    }