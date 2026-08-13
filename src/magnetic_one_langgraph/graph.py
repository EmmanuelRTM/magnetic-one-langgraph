"""Workflow graph wiring for the Magnetic-One LangGraph adaptation.

Topology: every worker agent reports back to the Orchestrator, which decides
the next hop dynamically (``Command``) until the task completes and the
FinalReview node produces the report.
"""

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from .agents import AGENT_NODES
from .orchestrator import finalize_task, orchestrator_agent
from .state import TaskState


def build_graph() -> CompiledStateGraph:
    """Build and compile the Magnetic-One task execution graph."""
    builder = StateGraph(TaskState)

    builder.add_node("Orchestrator", orchestrator_agent)
    for name, agent in AGENT_NODES.items():
        builder.add_node(name, agent)
    builder.add_node("FinalReview", finalize_task)

    builder.add_edge(START, "Orchestrator")
    # Workers always hand control back to the Orchestrator (inner loop).
    for name in AGENT_NODES:
        builder.add_edge(name, "Orchestrator")
    builder.add_edge("FinalReview", END)

    return builder.compile()
