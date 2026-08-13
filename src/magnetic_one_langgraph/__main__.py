"""Run the Magnetic-One task system from the command line.

Usage: python -m magnetic_one_langgraph "Describe the task here"
"""

import sys

from .runner import run_task_system

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) or "Analyze new market trends and compile a report."
    run_task_system(task)
