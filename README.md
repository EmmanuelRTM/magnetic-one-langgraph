# MagneticOne Multi-Agent System - Open-Source Exploration

Welcome to the open-source exploration of Microsoft’s MagneticOne multi-agent system! This repository provides a summarized workflow, a visual diagram, and an initial implementation in LangGraph. We encourage the community to contribute, test, and enhance this adaptation from Autogen to LangGraph.

---

## Overview

The MagneticOne multi-agent system, developed by Microsoft, is designed to enable efficient, multi-agent coordination and decision-making. This repository aims to:
1. Explain the workflow of MagneticOne in a concise format.
2. Provide a simple diagram to visualize the core process.
3. Present a first draft implementation of the workflow using LangGraph.

This project serves as a foundation for adapting Microsoft's work with Autogen to a LangGraph-based system.

## Background

The MagneticOne system is a **generalist multi-agent system** developed to solve complex, multi-step tasks through effective agent collaboration. For a deeper understanding of the original MagneticOne project, refer to the following resources provided by Microsoft:

- **Blog Post**: [Magnetic One: A Generalist Multi-Agent System for Solving Complex Tasks](https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/)
- **Research Paper**: [Magnetic One - Microsoft Research Paper (PDF)](https://www.microsoft.com/en-us/research/uploads/prod/2024/11/Magentic-One.pdf)
- **Official GitHub Repository**: [Autogen MagneticOne on GitHub](https://github.com/microsoft/autogen/tree/main/python/packages/autogen-magentic-one)

These references provide insights into the original design, architecture, and goals of MagneticOne, laying the groundwork for this open-source adaptation.

## Getting Started

To get involved, clone the repo, check out the LangGraph implementation, and run the tests to see it in action.

### Prerequisites

- **Python 3.10+**
- Familiarity with multi-agent systems is recommended.

### Installation

```bash
git clone https://github.com/EmmanuelRTM/magnetic-one-langgraph.git
cd magnetic-one-langgraph
pip install -e ".[test]"
```

This installs the package together with **LangGraph 1.x** and pytest. No API keys are required to run the scaffold — the agents are deterministic placeholders you can replace with LLM-backed implementations (`pip install -e ".[llm]"` adds `langchain` and `langchain-openai` for that).

### Usage

Run the demo task system from the command line:

```bash
python -m magnetic_one_langgraph "Analyze new market trends and compile a report."
```

or from Python:

```python
from magnetic_one_langgraph import build_graph, run_task_system

final_state = run_task_system("Analyze new market trends and compile a report.")
print(final_state["final_report"])
```

The [notebook](magnetic-one-langgraph.ipynb) walks through the workflow, the diagram, and the code step by step.

### Project layout

```
src/magnetic_one_langgraph/
├── state.py         # TypedDict state schema with reducers (messages, Task Ledger)
├── agents.py        # WebSurfer, FileSurfer, Coder, ComputerTerminal worker nodes
├── orchestrator.py  # Outer/inner loop: planning, stall detection, reflection, final report
├── graph.py         # StateGraph wiring (workers report back to the Orchestrator)
└── runner.py        # run_task_system entry point
tests/               # Unit and integration tests (pytest)
```

### Running the tests

```bash
pytest -v
```

The suite covers the state reducers, the Orchestrator's loop logic (completion, stall/reflection, replan budget), each worker agent, and an end-to-end graph run — including a regression test for [issue #1](https://github.com/EmmanuelRTM/magnetic-one-langgraph/issues/1) (`InvalidUpdateError: Must write to at least one of []`), which was caused by using a plain Python class as the graph state. Version `0.1.0` migrates the original `0.0.1` notebook draft to the LangGraph 1.x APIs: the state is now a `TypedDict` with reducers, nodes return partial updates, and the Orchestrator routes dynamically via `Command`.

### Contributing

Please check the following [CONTRIBUTING](CONTRIBUTING.md) file to know how to contribute to the project.

### Code of Conduct

Please check the following [CODE OF CONDUCT](CODE_OF_CONDUCT.md).

### License

This project is licensed under the [MIT License](LICENSE).