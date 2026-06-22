from langgraph.graph import (
    StateGraph,
    START,
    END
)

from state import AgentState

from nodes.router_node import router_node
from nodes.weather_node import weather_node
from nodes.response_node import response_node
from nodes.currency_node import (
    currency_node
)
from nodes.wiki_node import (
    wiki_node
)


builder = StateGraph(AgentState)

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "weather",
    weather_node
)

builder.add_node(
    "currency",
    currency_node
)

builder.add_node(
    "wiki",
    wiki_node
)



builder.add_node(
    "response",
    response_node
)

builder.add_edge(
    START,
    "router"
)

builder.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {
    "weather": "weather",
    "currency": "currency",
    "wiki": "wiki",
    "direct": "response"
}
)

builder.add_edge(
    "weather",
    "response"
)

builder.add_edge(
    "currency",
    "response"
)

builder.add_edge(
    "wiki",
    "response"
)

builder.add_edge(
    "response",
    END
)

graph = builder.compile()