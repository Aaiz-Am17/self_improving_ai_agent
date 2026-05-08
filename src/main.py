import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent.multi_agent_graph import build_multi_agent_graph
from langchain_core.messages import HumanMessage, SystemMessage

def main():

    graph = build_multi_agent_graph()

    query = "Analyze the dataset at data/datasets/titanic.csv and recommend preprocessing steps."

    messages = [
        SystemMessage(
            content="""
            You are an AI Data Science assistant.
            When analyzing datasets you should:
            1. Inspect dataset structure
            2. Check for missing values
            3. Analyze feature types
            Use the available tools when necessary.
            """
        ),
        HumanMessage(content=query)
    ]

    # Bumping the thread_id to ensure a clean slate for this run
    config = {
        "configurable": {
            "thread_id": "dataset_session_4" 
        }
    }

    print("\n===== AGENT EXECUTION TRACE =====\n")

    input_data = {"messages": messages}

    # The while loop keeps the script alive for multiple sequential tool calls
    while True:
        
        for step in graph.stream(input_data, config=config):
            for node, value in step.items():
                print(f"\n---- Node Executed: {node} ----\n")
                if "messages" in value:
                    for msg in value["messages"]:
                        # Safely print text, handling Gemini's occasional list/dict structure
                        if msg.content:
                            if isinstance(msg.content, list) and len(msg.content) > 0 and isinstance(msg.content[0], dict) and 'text' in msg.content[0]:
                                print(f"Content: {msg.content[0]['text']}")
                            else:
                                print(f"Content: {msg.content}")
                        
                        # Print requested tool calls
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            print(f"Tool Call Requested: {msg.tool_calls[0]['name']}")
                print("\n-----------------------------\n")

        # Check the state to see why the stream stopped
        state = graph.get_state(config)
        next_nodes = state.next

        # If next_nodes is empty, the graph reached the END node
        if not next_nodes:
            break

        # If it paused before the tools node, handle the HITL approval/editing
        if next_nodes[0] == "tools":
            
            # Grab the last message to see exactly what the agent planned to do
            last_msg = state.values["messages"][-1]
            tool_call = last_msg.tool_calls[0]
            
            print("\n⚠️ [HITL] GRAPH PAUSED: Agent is requesting to use a tool.")
            print(f"🔧 Proposed Tool: {tool_call['name']}")
            print(f"📦 Proposed Args: {tool_call['args']}")
            
            user_input = input("Approve (y), Cancel (n), or Edit (e)? ")
            
            if user_input.lower() == 'y':
                print("\n===== RESUMING EXECUTION =====\n")
                # Pass None to resume the interrupted graph
                input_data = None 
                
            elif user_input.lower() == 'e':
                # State Editing Logic
                current_path = tool_call['args'].get('file_path', '')
                new_path = input(f"Enter new file path (current: {current_path}): ")
                
                # Overwrite the argument in the message object
                last_msg.tool_calls[0]['args']['file_path'] = new_path
                
                # Update the graph's state memory directly with the modified message
                graph.update_state(config, {"messages": [last_msg]})
                
                print("\n===== STATE EDITED. RESUMING EXECUTION =====\n")
                input_data = None
                
            else:
                print("\nAction cancelled by user.")
                break

    print("\n===== EXECUTION COMPLETE =====\n")

if __name__ == "__main__":
    main()