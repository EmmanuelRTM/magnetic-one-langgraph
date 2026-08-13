"""Specialized worker agents of the Magnetic-One system.

Each agent is a LangGraph node: it receives the current :class:`TaskState`
and returns a *partial update* (never a mutated state object). The agents
here are deterministic scaffolds mirroring the original notebook; wire in
LLM calls or tools (web search, file readers, code executors) by replacing
the body of the relevant function while keeping the same update contract.
"""

from .state import TaskState

# Ledger key each agent is expected to fill in. The Orchestrator uses this
# mapping both to detect progress and to decide when the task is complete.
AGENT_LEDGER_KEYS: dict[str, str] = {
    "WebSurfer": "web_data",
    "FileSurfer": "file_data",
    "Coder": "code_analysis",
    "ComputerTerminal": "execution_result",
}


def web_surfer_agent(state: TaskState) -> TaskState:
    """Gathers data from the web and updates the Task Ledger."""
    return {
        "messages": ["WebSurfer is gathering data from the web."],
        "task_ledger": {"web_data": "Sample web data retrieved"},
    }


def file_surfer_agent(state: TaskState) -> TaskState:
    """Reads files and updates the Task Ledger."""
    return {
        "messages": ["FileSurfer is reading files."],
        "task_ledger": {"file_data": "Sample file data retrieved"},
    }


def coder_agent(state: TaskState) -> TaskState:
    """Analyzes or debugs code as required by the task."""
    return {
        "messages": ["Coder is analyzing code."],
        "task_ledger": {"code_analysis": "Code analyzed successfully."},
    }


def computer_terminal_agent(state: TaskState) -> TaskState:
    """Executes necessary commands or installs libraries."""
    return {
        "messages": ["ComputerTerminal is executing commands."],
        "task_ledger": {"execution_result": "Commands executed successfully."},
    }


AGENT_NODES = {
    "WebSurfer": web_surfer_agent,
    "FileSurfer": file_surfer_agent,
    "Coder": coder_agent,
    "ComputerTerminal": computer_terminal_agent,
}
