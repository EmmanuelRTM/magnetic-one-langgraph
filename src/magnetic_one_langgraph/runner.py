"""Convenience entry point to run the Magnetic-One task system."""

from langgraph.graph.state import CompiledStateGraph

from .graph import build_graph
from .state import TaskState, initial_state


def run_task_system(
    task_description: str,
    graph: CompiledStateGraph | None = None,
    verbose: bool = True,
) -> TaskState:
    """Execute the task system for ``task_description`` and return the final state.

    Streams orchestration messages as they are produced when ``verbose``.
    """
    graph = graph or build_graph()

    final_state: TaskState = {}
    printed = 0
    for snapshot in graph.stream(initial_state(task_description), stream_mode="values"):
        final_state = snapshot
        if verbose:
            messages = snapshot.get("messages", [])
            for message in messages[printed:]:
                print(message)
            printed = len(messages)

    if verbose and final_state.get("final_report"):
        print("Task Complete" if final_state.get("task_complete") else "Task Ended")
        print(final_state["final_report"])
    return final_state
