from langgraph.graph import StateGraph
from langgraph.graph import START, END

from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from state import State

from nodes.agent_node import agent_node
from tools.api_tools import TOOLS


builder = StateGraph(State)


builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tools",
    ToolNode(TOOLS)
)


builder.add_edge(
    START,
    "agent"
)


builder.add_conditional_edges(
    "agent",
    tools_condition
)


builder.add_edge(
    "tools",
    "agent"
)


graph = builder.compile()