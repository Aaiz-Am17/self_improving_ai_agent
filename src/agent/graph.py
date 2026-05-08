from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage

from src.tools.tools import inspect_dataset, detect_missing_values

from langgraph.graph.message import add_messages



# ------------------------------
# STATE
# ------------------------------

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ------------------------------
# LLM (Updated for Gemini)
# ------------------------------
# Using 'gemini-2.5-flash' or 'gemini-1.5-flash' as the fast, cost-effective equivalent to gpt-4o-mini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", #
    temperature=0,
    google_api_key="AIzaSyCoUhK2Fnh9BmGN3aCqVufPgIygyrcv6B8" 
)

# ------------------------------
# TOOLS
# ------------------------------
tools = [inspect_dataset, detect_missing_values]

# Gemini supports LangChain's standard tool binding perfectly
llm_with_tools = llm.bind_tools(tools)


# ------------------------------
# AGENT NODE
# ------------------------------

def agent_node(state: AgentState):

    messages = state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


# ------------------------------
# TOOL NODE
# ------------------------------

tool_node = ToolNode(tools)


# ------------------------------
# ROUTER
# ------------------------------

def router(state: AgentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tool"

    return END


# ------------------------------
# GRAPH
# ------------------------------

def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tool", tool_node)

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        router,
        {
            "tool": "tool",
            END: END,
        },
    )

    graph.add_edge("tool", "agent")

    return graph.compile()
