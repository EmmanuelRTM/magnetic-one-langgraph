"""Magnetic-One multi-agent workflow adapted to LangGraph."""

from .agents import (
    AGENT_LEDGER_KEYS,
    AGENT_NODES,
    coder_agent,
    computer_terminal_agent,
    file_surfer_agent,
    web_surfer_agent,
)
from .graph import build_graph
from .orchestrator import (
    DEFAULT_PLAN,
    MAX_REPLANS,
    STALL_THRESHOLD,
    create_task_ledger,
    evaluate_completion,
    finalize_task,
    generate_task_plan,
    orchestrator_agent,
    reflect_and_adjust,
)
from .runner import run_task_system
from .state import TaskState, initial_state, merge_dicts

__version__ = "0.1.0"

__all__ = [
    "AGENT_LEDGER_KEYS",
    "AGENT_NODES",
    "DEFAULT_PLAN",
    "MAX_REPLANS",
    "STALL_THRESHOLD",
    "TaskState",
    "build_graph",
    "coder_agent",
    "computer_terminal_agent",
    "create_task_ledger",
    "evaluate_completion",
    "file_surfer_agent",
    "finalize_task",
    "generate_task_plan",
    "initial_state",
    "merge_dicts",
    "orchestrator_agent",
    "reflect_and_adjust",
    "run_task_system",
    "web_surfer_agent",
]
