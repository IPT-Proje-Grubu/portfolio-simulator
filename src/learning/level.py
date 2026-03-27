"""Level class — a named progression tier containing ordered Tasks."""

from __future__ import annotations

from src.learning.task import Task


class Level:
    """
    A learning level (e.g. Beginner) that owns an ordered list of Tasks.

    Mutable state (which tasks are complete, total XP) is tracked externally
    by LearningManager and passed in as arguments so this class stays stateless
    and easily serialisable.
    """

    def __init__(
        self,
        id: str,
        name: str,
        icon: str,
        xp_required: int,
        tasks: list[Task],
    ) -> None:
        self.id           = id
        self.name         = name
        self.icon         = icon
        self.xp_required  = xp_required  # XP needed to unlock this level
        self.tasks        = tasks

    # ── Queries (require external state) ─────────────────────────────────────

    def is_unlocked(self, total_xp: int) -> bool:
        return total_xp >= self.xp_required

    def completed_count(self, done: set[str]) -> int:
        return sum(1 for t in self.tasks if t.id in done)

    def total_task_count(self) -> int:
        return len(self.tasks)

    def is_complete(self, done: set[str]) -> bool:
        return all(t.id in done for t in self.tasks)

    def get_next_task(self, done: set[str]) -> Task | None:
        """Return the first incomplete task (the current active task)."""
        for task in self.tasks:
            if task.id not in done:
                return task
        return None

    def is_task_locked(self, task: Task, done: set[str], total_xp: int) -> bool:
        """
        A task is locked if:
        (a) the level itself is locked (insufficient XP), or
        (b) the task before it in the list is not yet complete.
        """
        if not self.is_unlocked(total_xp):
            return True
        idx = next((i for i, t in enumerate(self.tasks) if t.id == task.id), 0)
        if idx == 0:
            return False
        return self.tasks[idx - 1].id not in done

    def earned_xp(self, done: set[str]) -> int:
        return sum(t.xp for t in self.tasks if t.id in done)

    def max_xp(self) -> int:
        return sum(t.xp for t in self.tasks)

    def __repr__(self) -> str:
        return f"Level(id={self.id!r}, name={self.name!r}, tasks={len(self.tasks)})"
