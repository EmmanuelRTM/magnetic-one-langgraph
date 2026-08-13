"""Unit tests for the specialized worker agents."""

import pytest

from magnetic_one_langgraph.agents import AGENT_LEDGER_KEYS, AGENT_NODES


@pytest.mark.parametrize("name", sorted(AGENT_NODES))
def test_agent_returns_partial_update_with_expected_ledger_key(name):
    agent = AGENT_NODES[name]
    update = agent({})

    # Nodes must return partial updates (dicts), never a mutated state object.
    assert isinstance(update, dict)
    assert AGENT_LEDGER_KEYS[name] in update["task_ledger"]
    assert len(update["messages"]) == 1


def test_every_agent_has_a_ledger_key_mapping():
    assert set(AGENT_NODES) == set(AGENT_LEDGER_KEYS)
