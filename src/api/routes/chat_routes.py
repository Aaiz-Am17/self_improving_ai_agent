from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from src.agent.graph import graph
from src.api.schemas.chat_schema import ChatRequest

router = APIRouter()

@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    
    config = {"configurable": {"thread_id": request.thread_id}}
    
    # CASE 1: RESUMING FROM A PAUSE (User clicked Approve/Reject)
    if request.approval_decision:
        # Update the state with the human's decision
        graph.update_state(
            config, 
            {"human_feedback": {"approval": request.approval_decision}, "runtime_mode": "api"}, 
            as_node="pipeline_architect"
        )
        # Resume the graph with None as input
        result = graph.invoke(None, config=config)
    
    # CASE 2: NEW CHAT MESSAGE
    else:
        initial_state = {
            "messages": [HumanMessage(content=request.message)],
            "dataset_path": request.dataset_path,
            "thread_id": request.thread_id,
            "runtime_mode": "api"
        }
        result = graph.invoke(initial_state, config=config)

    # Check if the graph is currently paused
    state_snapshot = graph.get_state(config)
    needs_approval = len(state_snapshot.next) > 0 and state_snapshot.next[0] == "validator"

    return {
        "response": result,
        "needs_approval": needs_approval
    }