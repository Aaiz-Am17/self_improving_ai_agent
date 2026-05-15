from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json

from langchain_core.messages import HumanMessage
from src.agent.graph import graph
from src.api.schemas.chat_schema import ChatRequest

router = APIRouter()

@router.post("/stream")
async def stream_endpoint(request: ChatRequest):

    initial_state = {
        "messages": [
            HumanMessage(content=request.message)
        ],
        "dataset_path": request.dataset_path,
        "thread_id": request.thread_id,
        "runtime_mode": "api"
    }

    config = {"configurable": {"thread_id": request.thread_id}}

    async def event_generator():
        try:
            # Yields state updates as each LangGraph node completes
            async for event in graph.astream(initial_state, config=config):
                for node, state in event.items():
                    payload = {
                        "node": node, 
                        "status": "processing"
                    }
                    yield f"data: {json.dumps(payload)}\n\n"
                    
            yield f"data: {json.dumps({'node': 'END', 'status': 'completed'})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")