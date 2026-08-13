"""Unit tests for the Orchestrator's outer/inner-loop logic."""

from magnetic_one_langgraph.orchestrator import (
    DEFAULT_PLAN,
    MAX_REPLANS,
    STALL_THRESHOLD,
    create_task_ledger,
    evaluate_completion,
    finalize_task,
    orchestrator_agent,
    reflect_and_adjust,
)
from magnetic_one_langgraph.state import initial_state


def full_ledger() -> dict[str, str]:
    return {
        "task_id": "001",
        "web_data": "w",
        "file_data": "f",
        "code_analysis": "c",
        "execution_result": "e",
    }


def test_first_visit_sets_up_ledger_and_dispatches_first_step():
    command = orchestrator_agent(initial_state("demo task"))

    assert command.goto == DEFAULT_PLAN[0][0]
    assert command.update["task_ledger"]["task"] == "demo task"
    assert command.update["task_plan"] == DEFAULT_PLAN[1:]
    assert any("set up the task and plan" in m for m in command.update["messages"])


def test_completion_routes_to_final_review():
    state = initial_state("demo")
    state["task_ledger"] = full_ledger()
    command = orchestrator_agent(state)

    assert command.goto == "FinalReview"
    assert command.update["task_complete"] is True


def test_progress_dispatches_next_planned_agent_and_resets_counter():
    state = initial_state("demo")
    state["task_ledger"] = {"task_id": "001", "web_data": "w"}
    state["task_plan"] = [("FileSurfer", "Read from files")]
    state["last_ledger_size"] = 1  # ledger grew since last dispatch
    state["counter"] = 1
    command = orchestrator_agent(state)

    assert command.goto == "FileSurfer"
    assert command.update["counter"] == 0
    assert command.update["task_plan"] == []


def test_stall_triggers_reflection_and_replan():
    state = initial_state("demo")
    state["task_ledger"] = {"task_id": "001"}
    state["task_plan"] = [("Coder", "Analyze data")]
    state["last_ledger_size"] = 1  # no progress since last dispatch
    state["counter"] = STALL_THRESHOLD - 1
    command = orchestrator_agent(state)

    # Reflection rebuilds the plan from the missing steps and re-dispatches.
    assert command.goto == DEFAULT_PLAN[0][0]
    assert command.update["replans"] == 1
    assert command.update["counter"] == 0
    assert any("reflecting due to stall" in m for m in command.update["messages"])


def test_exhausted_replan_budget_falls_back_to_best_guess():
    state = initial_state("demo")
    state["task_ledger"] = {"task_id": "001"}
    state["task_plan"] = []
    state["last_ledger_size"] = 1
    state["replans"] = MAX_REPLANS
    command = orchestrator_agent(state)

    assert command.goto == "FinalReview"
    assert command.update["task_complete"] is False


def test_reflect_and_adjust_keeps_only_missing_steps():
    state = initial_state("demo")
    state["task_ledger"] = {"web_data": "w", "code_analysis": "c"}
    plan = reflect_and_adjust(state)

    assert [agent for agent, _ in plan] == ["FileSurfer", "ComputerTerminal"]
    assert all(instruction.startswith("Re-attempt:") for _, instruction in plan)


def test_evaluate_completion_requires_every_capability():
    state = initial_state("demo")
    assert evaluate_completion(state) is False
    state["task_ledger"] = full_ledger()
    assert evaluate_completion(state) is True


def test_create_task_ledger_records_task_description():
    ledger = create_task_ledger(initial_state("special task"))
    assert ledger["task"] == "special task"
    assert "known_facts" in ledger and "guesses" in ledger


def test_finalize_task_reports_ledger_contents():
    state = initial_state("demo")
    state["task_ledger"] = full_ledger()
    state["task_complete"] = True
    update = finalize_task(state)

    assert "Final Report" in update["final_report"]
    assert "Web Data: w" in update["final_report"]
    assert update["messages"] == ["Final report generated."]


def test_finalize_task_incomplete_reports_best_guess():
    state = initial_state("demo")
    state["task_ledger"] = {"task_id": "001"}
    update = finalize_task(state)

    assert "Best Educated Guess" in update["final_report"]
