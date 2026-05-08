import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent.multi_agent_graph import build_multi_agent_graph
from langchain_core.messages import HumanMessage

def main():
    graph = build_multi_agent_graph()

    # Bumping the thread_id so we get a clean test
    config = {
        "configurable": {
            "thread_id": "memory_test_thread_2" 
        }
    }

    print("\n" + "="*50)
    print(" SESSION 1: INTRODUCING INFORMATION")
    print("="*50 + "\n")

    query_1 = "Hi, my name is Aaiz. I am going to be working on the housing dataset today. Don't analyze it yet, just say hello and confirm you know my name and the dataset."
    print(f"User: {query_1}\n")
    
    for step in graph.stream({"messages": [HumanMessage(content=query_1)]}, config=config):
        for node, value in step.items():
            if "messages" in value:
                for msg in value["messages"]:
                    # Check that there is content AND it is not actively making a tool call
                    if msg.content and not (hasattr(msg, "tool_calls") and msg.tool_calls):
                        # Handle Gemini's payload structure
                        if isinstance(msg.content, list) and len(msg.content) > 0 and isinstance(msg.content[0], dict) and 'text' in msg.content[0]:
                            print(f"Agent ({node}): {msg.content[0]['text']}\n")
                        else:
                            print(f"Agent ({node}): {msg.content}\n")

    print("="*50)
    print(" SIMULATING SCRIPT RESTART...")
    print("="*50 + "\n")

    query_2 = "What is my name, and which dataset did I say I was working on?"
    print(f"User: {query_2}\n")

    for step in graph.stream({"messages": [HumanMessage(content=query_2)]}, config=config):
        for node, value in step.items():
            if "messages" in value:
                for msg in value["messages"]:
                    if msg.content and not (hasattr(msg, "tool_calls") and msg.tool_calls):
                        if isinstance(msg.content, list) and len(msg.content) > 0 and isinstance(msg.content[0], dict) and 'text' in msg.content[0]:
                            print(f"Agent ({node}): {msg.content[0]['text']}\n")
                        else:
                            print(f"Agent ({node}): {msg.content}\n")

    print("="*50)
    print(" MEMORY TEST COMPLETE")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()