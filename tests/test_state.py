"""Unit tests for the state schema and its reducers."""

from magnetic_one_langgraph.state import initial_state, merge_dicts


def test_merge_dicts_merges_and_overrides():
    assert merge_dicts({"a": "1", "b": "2"}, {"b": "3", "c": "4"}) == {
        "a": "1",
        "b": "3",
        "c": "4",
    }


def test_merge_dicts_handles_none_operands():
    assert merge_dicts(None, {"a": "1"}) == {"a": "1"}
    assert merge_dicts({"a": "1"}, None) == {"a": "1"}


def test_initial_state_seeds_all_channels():
    state = initial_state("Do the thing")
    assert state["task_description"] == "Do the thing"
    assert state["messages"] == ["Task started: Do the thing"]
    assert state["task_ledger"] == {}
    assert state["task_plan"] == []
    assert state["counter"] == 0
    assert state["replans"] == 0
    assert state["task_complete"] is False
    assert state["final_report"] is None
