"""Backwards-compatibility shim.

All real logic has moved to:
  src/learning/manager.py   → LearningManager
  src/learning/task.py      → Task, TaskStatus
  src/learning/level.py     → Level

This file re-exports everything under the old names so that existing imports
(main_window.py, learn_page.py) continue to work without modification.
"""

from src.learning.manager import (
    Achievement,
    Challenge,
    LearningExtra,
    LearningManager,
)
from src.learning.task import Task, TaskStatus

# ── Backwards-compatible aliases ──────────────────────────────────────────────

LearningSystem = LearningManager   # old name → new name
TaskSpec       = Task              # old name → new name

__all__ = [
    "Achievement",
    "Challenge",
    "LearningExtra",
    "LearningManager",
    "LearningSystem",
    "Task",
    "TaskSpec",
    "TaskStatus",
]
