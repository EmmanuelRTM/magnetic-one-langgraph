"""The Orchestrator: outer-loop setup and inner-loop coordination.

Outer loop: on the first visit the Orchestrator creates the Task Ledger
(facts, lookups, guesses) and derives a step-by-step plan from the available
agent roles.

Inner loop: on every subsequent visit it evaluates completion, checks for
stalls (no new Task Ledger entries since the last dispatch), reflects and
re-plans when the stall counter exceeds its threshold, and otherwise
dispatches the next agent with its instruction via a ``Command``.
"""

from typing import Literal

from langgraph.types import Command

from .agents import AGENT_LEDGER_KEYS
from .state import PlanStep, TaskState

# Inner-loop tuning knobs, mirroring the thresholds of the original draft.
STALL_THRESHOLD = 2
MAX_REPLANS = 2

DEFAULT_PLAN: list[PlanStep] = [
    ("WebSurfer", "Perform web search"),
    ("FileSurfer", "Read from files"),
    ("Coder", "Analyze data"),
    ("ComputerTerminal", "Execute necessary commands"),
]

OrchestratorTarget = Literal[
    "WebSurfer", "FileSurfer", "Coder", "ComputerTerminal", "FinalReview"
]


def create_task_ledger(state: TaskState) -> dict[str, str]:
    """Populates the Task Ledger with initial facts and guesses."""
    return {
        "task_id": "001",
        "task": state.get("task_description", "Unspecified task"),
        "known_facts": "Initial task facts",
        "guesses": "Potential unknown elements",
    }


def generate_task_plan(state: TaskState) -> list[PlanStep]:
    """Generates a step-by-step task plan based on the Task Ledger and roles."""
    return list(DEFAULT_PLAN)


def evaluate_completion(state: TaskState) -> bool:
    """The task is complete once every agent capability delivered its data."""
    ledger = state.get("task_ledger") or {}
    return all(key in ledger for key in AGENT_LEDGER_KEYS.values())


def reflect_and_adjust(state: TaskState) -> list[PlanStep]:
    """Rebuild the plan, keeping only the steps whose results are missing."""
    ledger = state.get("task_ledger") or {}
    return [
        (agent, f"Re-attempt: {instruction}")
        for agent, instruction in DEFAULT_PLAN
        if AGENT_LEDGER_KEYS[agent] not in ledger
    ]


def orchestrator_agent(state: TaskState) -> Command[OrchestratorTarget]:
    """Single Orchestrator node driving both the outer and the inner loop."""
    ledger = state.get("task_ledger") or {}
    messages: list[str] = []
    update: TaskState = {}

    # Outer loop: first visit sets up the Task Ledger and the plan.
    if not ledger:
        update["task_ledger"] = create_task_ledger(state)
        plan = generate_task_plan(state)
        messages.append("Orchestrator has set up the task and plan.")
        counter = 0
        replans = state.get("replans", 0)
    else:
        plan = list(state.get("task_plan") or [])
        replans = state.get("replans", 0)

        # Inner loop: evaluate task completion first.
        if evaluate_completion(state):
            messages.append("Orchestrator confirmed the task is complete.")
            update["messages"] = messages
            update["task_complete"] = True
            return Command(goto="FinalReview", update=update)

        # Stall detection: did the last dispatched agent add ledger entries?
        made_progress = len(ledger) > state.get("last_ledger_size", 0)
        counter = 0 if made_progress else state.get("counter", 0) + 1

        needs_reflection = counter >= STALL_THRESHOLD or not plan
        if needs_reflection:
            if replans >= MAX_REPLANS:
                messages.append(
                    "Replan budget exhausted; reporting best educated guess."
                )
                update["messages"] = messages
                update["task_complete"] = False
                return Command(goto="FinalReview", update=update)
            messages.append("Orchestrator reflecting due to stall.")
            messages.append("Revisiting task plan and refining approach.")
            plan = reflect_and_adjust(state)
            replans += 1
            counter = 0

    # Dispatch the next agent with its instruction.
    next_agent, instruction = plan[0]
    messages.append(f"Orchestrator directs {next_agent}: {instruction}")
    update.update(
        {
            "messages": messages,
            "task_plan": plan[1:],
            "counter": counter,
            "replans": replans,
            "last_ledger_size": len(ledger) + len(update.get("task_ledger") or {}),
        }
    )
    return Command(goto=next_agent, update=update)


def finalize_task(state: TaskState) -> TaskState:
    """Generates the final report (or best educated guess) from the Task Ledger."""
    ledger = state.get("task_ledger") or {}
    header = (
        "Final Report" if state.get("task_complete") else "Best Educated Guess"
    )
    report_lines = [
        f"{header}",
        f"Task ID: {ledger.get('task_id')}",
        f"Task: {ledger.get('task')}",
        f"Known Facts: {ledger.get('known_facts')}",
        f"Web Data: {ledger.get('web_data')}",
        f"File Data: {ledger.get('file_data')}",
        f"Code Analysis: {ledger.get('code_analysis')}",
        f"Execution Result: {ledger.get('execution_result')}",
        f"Uncertainties: {ledger.get('guesses')}",
    ]
    return {
        "messages": ["Final report generated."],
        "final_report": "\n".join(report_lines),
    }
