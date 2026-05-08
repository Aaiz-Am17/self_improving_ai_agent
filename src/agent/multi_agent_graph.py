from typing import TypedDict, Annotated
import sqlite3
import os

from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.prebuilt import ToolNode
from src.tools.tools import inspect_dataset, detect_missing_values, analyze_features
from langgraph.checkpoint.sqlite import SqliteSaver


# ------------------------------
# STATE
# ------------------------------

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ------------------------------
# LLM
# ------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key="AIzaSyCoUhK2Fnh9BmGN3aCqVufPgIygyrcv6B8"  
)


# ------------------------------
# TOOLS
# ------------------------------

tools = [
    inspect_dataset,
    detect_missing_values,
    analyze_features
]

tool_node = ToolNode(tools)

llm_with_tools = llm.bind_tools(tools)


# ------------------------------
# RESEARCHER AGENT
# ------------------------------

def researcher_node(state: AgentState):

    messages = state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


# ------------------------------
# ANALYST AGENT
# ------------------------------

def analyst_node(state: AgentState):

    messages = state["messages"]

    system_prompt = SystemMessage(
        content="""
You are a Data Science Analyst.

Using the dataset information gathered by the Researcher,
generate:

• Data quality observations
• Recommended preprocessing steps
• Suggested ML model types
"""
    )

    response = llm.invoke([system_prompt] + messages)

    return {"messages": [response]}


# ------------------------------
# ROUTER
# ------------------------------

def researcher_router(state: AgentState):

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return "analyst"


# ------------------------------
# GRAPH
# ------------------------------

def build_multi_agent_graph():

    builder = StateGraph(AgentState)

    builder.add_node("researcher", researcher_node)
    builder.add_node("tools", tool_node)
    builder.add_node("analyst", analyst_node)

    builder.set_entry_point("researcher")

    builder.add_conditional_edges(
        "researcher",
        researcher_router,
        {
            "tools": "tools",
            "analyst": "analyst"
        }
    )

    builder.add_edge("tools", "researcher")
    builder.add_edge("analyst", END)

    # ------------------------------
    # SQLITE MEMORY (SAFE VERSION)
    # ------------------------------

    conn = sqlite3.connect("checkpoint_db.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)

    graph = builder.compile(
        checkpointer=memory,
        interrupt_before=["tools"]
    )

    return graph