"""Integration tests running the compiled graph end to end."""

from magnetic_one_langgraph import build_graph, run_task_system
from magnetic_one_langgraph.state import initial_state


def test_graph_runs_to_completion():
    graph = build_graph()
    result = graph.invoke(initial_state("Analyze new market trends."))

    assert result["task_complete"] is True
    assert "Final Report" in result["final_report"]
    # Every agent contributed to the Task Ledger.
    for key in ("web_data", "file_data", "code_analysis", "execution_result"):
        assert key in result["task_ledger"]


def test_agents_run_in_planned_order():
    graph = build_graph()
    result = graph.invoke(initial_state("demo"))
    text = "\n".join(result["messages"])

    assert text.index("WebSurfer is") < text.index("FileSurfer is")
    assert text.index("FileSurfer is") < text.index("Coder is")
    assert text.index("Coder is") < text.index("ComputerTerminal is")
    assert result["messages"][-1] == "Final report generated."


def test_streaming_yields_updates_without_invalid_update_error():
    """Regression test for GitHub issue #1.

    The original notebook streamed a plain class instance through the graph,
    which raised ``InvalidUpdateError: Must write to at least one of []``.
    With a proper TypedDict schema and partial updates, streaming works.
    """
    graph = build_graph()
    steps = list(
        graph.stream(initial_state("demo"), stream_mode="updates")
    )

    assert steps, "streaming should yield at least one update"
    visited = [node for step in steps for node in step]
    assert visited[0] == "Orchestrator"
    assert visited[-1] == "FinalReview"


def test_run_task_system_prints_progress_and_returns_state(capsys):
    result = run_task_system("Compile a report.")
    output = capsys.readouterr().out

    assert "Task started: Compile a report." in output
    assert "Task Complete" in output
    assert "Final Report" in output
    assert result["task_complete"] is True


def test_run_task_system_quiet_mode(capsys):
    result = run_task_system("Silent run.", verbose=False)

    assert capsys.readouterr().out == ""
    assert result["final_report"]
