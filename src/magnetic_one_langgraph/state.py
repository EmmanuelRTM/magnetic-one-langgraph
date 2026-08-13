"""State schema for the Magnetic-One LangGraph workflow.

The original notebook used a plain Python class as the graph state, which is
not a valid LangGraph state schema and caused
``langgraph.errors.InvalidUpdateError: Must write to at least one of []``
(see GitHub issue #1). LangGraph expects a ``TypedDict`` (or Pydantic model)
whose keys become channels; nodes then return *partial updates* instead of
mutating a shared object.
"""

from operator import add
from typing import Annotated, Optional, TypedDict


def merge_dicts(left: dict[str, str], right: dict[str, str]) -> dict[str, str]:
    """Reducer merging partial Task Ledger updates into the existing ledger."""
    return {**(left or {}), **(right or {})}


# A plan step pairs an agent node name with the instruction it should follow.
PlanStep = tuple[str, str]


class TaskState(TypedDict, total=False):
    """Shared state flowing through the Magnetic-One graph.

    ``messages`` and ``task_ledger`` carry reducers so every node can
    contribute updates without overwriting what other nodes wrote.
    """

    task_description: str
    messages: Annotated[list[str], add]
    task_ledger: Annotated[dict[str, str], merge_dicts]  # facts, guesses, agent results
    task_plan: list[PlanStep]  # remaining step-by-step plan
    counter: int  # stall counter for the inner loop
    replans: int  # how many times the plan was rebuilt via reflection
    last_ledger_size: int  # used by the Orchestrator to detect progress
    task_complete: bool
    final_report: Optional[str]


def initial_state(task_description: str) -> TaskState:
    """Build the seed state handed to the graph for a new task."""
    return TaskState(
        task_description=task_description,
        messages=[f"Task started: {task_description}"],
        task_ledger={},
        task_plan=[],
        counter=0,
        replans=0,
        last_ledger_size=0,
        task_complete=False,
        final_report=None,
    )
