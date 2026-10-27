from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


@dataclass
class Owner:
    owner_id: int
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care list."""
        if pet not in self.pets:
            self.pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return this owner's pets."""
        return list(self.pets)

    def get_all_tasks(self) -> list[Task]:
        """Return tasks from every pet owned by this owner."""
        return [task for pet in self.pets for task in pet.get_tasks()]


@dataclass
class Pet:
    pet_id: int
    name: str
    age: int
    breed: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        if task not in self.tasks:
            self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return list(self.tasks)


@dataclass
class Task:
    title: str
    # datetime carries both the scheduled date and time; date remains accepted
    # for simple all-day tasks and compatibility with the initial UML.
    due_date: date | datetime
    priority: str
    recurrence_frequency: str = "none"
    duration_minutes: int = 0
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for an owner."""
        self.owner = owner
        # This is a refreshed view of the pets' task lists, not the source data.
        self.tasks: list[Task] = owner.get_all_tasks()

    def _refresh_tasks(self) -> list[Task]:
        """Update the task list from the owner's pets."""
        self.tasks = self.owner.get_all_tasks()
        return self.tasks

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler's current view."""
        if task not in self.tasks:
            self.tasks.append(task)

    def sort_tasks(self) -> list[Task]:
        """Sort the owner's tasks by scheduled time, then priority."""
        priority_order = {"high": 0, "medium": 1, "low": 2}

        def sort_key(task: Task) -> tuple[datetime, int]:
            """Get the time and priority used to sort a task."""
            scheduled = task.due_date
            if isinstance(scheduled, datetime):
                scheduled_at = scheduled
            else:
                scheduled_at = datetime.combine(scheduled, datetime.min.time())
            return scheduled_at, priority_order.get(task.priority.lower(), 3)

        self._refresh_tasks()
        self.tasks.sort(key=sort_key)
        return list(self.tasks)

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of tasks whose scheduled time ranges overlap."""
        tasks = self.sort_tasks()
        conflicts: list[tuple[Task, Task]] = []
        for index, first in enumerate(tasks):
            first_start = _as_datetime(first.due_date)
            first_end = first_start + timedelta(minutes=max(0, first.duration_minutes))
            for second in tasks[index + 1 :]:
                second_start = _as_datetime(second.due_date)
                second_end = second_start + timedelta(minutes=max(0, second.duration_minutes))
                if first_start < second_end and second_start < first_end:
                    conflicts.append((first, second))
        return conflicts

    def get_upcoming_tasks(self) -> list[Task]:
        """Return incomplete tasks scheduled now or in the future, in order."""
        now = datetime.now()
        upcoming = [
            task for task in self._refresh_tasks()
            if not task.completed and _as_datetime(task.due_date) >= now
        ]
        priority_order = {"high": 0, "medium": 1, "low": 2}
        upcoming.sort(
            key=lambda task: (
                _as_datetime(task.due_date),
                priority_order.get(task.priority.lower(), 3),
            )
        )
        return upcoming


def _as_datetime(value: date | datetime) -> datetime:
    """Convert a date or datetime value to a datetime."""
    if isinstance(value, datetime):
        return value
    return datetime.combine(value, datetime.min.time())
