from langgraph.graph import StateGraph, END

from app.graph.state import GraphState
from app.graph.nodes import retrieve_node, fetch_stock_node, generate_node


def route_after_retrieve(state: GraphState) -> str:
    """
    Conditional edge: decides whether to fetch live stock data or go
    straight to generation. This is the explicit, inspectable version
    of the "if request.stock_ticker:" check - now it's graph structure,
    not a buried conditional inside a function body.
    """
    if state.get("stock_ticker"):
        return "fetch_stock"
    return "generate"


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("fetch_stock", fetch_stock_node)
    graph.add_node("generate", generate_node)

    graph.set_entry_point("retrieve")

    graph.add_conditional_edges(
        "retrieve",
        route_after_retrieve,
        {
            "fetch_stock": "fetch_stock",
            "generate": "generate",
        },
    )

    graph.add_edge("fetch_stock", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


# Compiled once at import time, reused across requests - compiling the
# graph is a one-time cost, not something to redo per-request.
compiled_graph = build_graph()
