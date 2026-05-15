from fastapi import APIRouter, HTTPException
import asyncio

from langchain_core.messages import HumanMessage
from src.agent.graph import graph
from src.api.schemas.chat_schema import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):

    initial_state = {
        "messages": [
            HumanMessage(content=request.message)
        ],
        "dataset_path": request.dataset_path,
        "thread_id": request.thread_id,
        "runtime_mode": "api"  # Bypasses the headless input() error
    }

    # Required for LangGraph memory persistence
    config = {"configurable": {"thread_id": request.thread_id}}

    try:
        # Run graph in a separate thread to avoid blocking FastAPI's event loop
        result = await asyncio.to_thread(graph.invoke, initial_state, config)

        return {
            "response": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))