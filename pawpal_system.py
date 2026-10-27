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

    def sort_by_time(self) -> list[Task]:
        """Return all owner tasks ordered by scheduled date and time."""
        return sorted(self._refresh_tasks(), key=lambda task: _as_datetime(task.due_date))

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

        return sorted(self._refresh_tasks(), key=sort_key)

    def filter_tasks(
        self, *, pet_name: str | None = None, completed: bool | None = None
    ) -> list[Task]:
        """Filter tasks by pet name and/or completion status."""
        pets_by_task = {
            id(task): pet
            for pet in self.owner.get_pets()
            for task in pet.get_tasks()
        }
        tasks = self._refresh_tasks()
        if pet_name is not None:
            wanted_name = pet_name.strip().casefold()
            tasks = [
                task for task in tasks
                if pets_by_task.get(id(task))
                and pets_by_task[id(task)].name.casefold() == wanted_name
            ]
        if completed is not None:
            tasks = [task for task in tasks if task.completed is completed]
        return sorted(tasks, key=lambda task: _as_datetime(task.due_date))

    def mark_task_complete(self, task: Task) -> Task | None:
        """Complete a task and add its next daily or weekly occurrence."""
        pet = next(
            (pet for pet in self.owner.get_pets() if any(saved is task for saved in pet.get_tasks())),
            None,
        )
        if pet is None:
            raise ValueError("Task does not belong to a pet owned by this scheduler.")

        task.mark_complete()
        frequency = task.recurrence_frequency.strip().casefold()
        days = {"daily": 1, "weekly": 7}.get(frequency)
        if days is None:
            self._refresh_tasks()
            return None

        next_due = task.due_date + timedelta(days=days)
        next_task = Task(
            title=task.title,
            due_date=next_due,
            priority=task.priority,
            recurrence_frequency=task.recurrence_frequency,
            duration_minutes=task.duration_minutes,
        )
        pet.add_task(next_task)
        self._refresh_tasks()
        return next_task

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs with overlapping durations or identical start times."""
        tasks = self.sort_tasks()
        conflicts: list[tuple[Task, Task]] = []
        for index, first in enumerate(tasks):
            first_start = _as_datetime(first.due_date)
            first_end = first_start + timedelta(minutes=max(0, first.duration_minutes))
            for second in tasks[index + 1 :]:
                second_start = _as_datetime(second.due_date)
                second_end = second_start + timedelta(minutes=max(0, second.duration_minutes))
                same_start = first_start == second_start
                overlaps = first_start < second_end and second_start < first_end
                if same_start or overlaps:
                    conflicts.append((first, second))
        return conflicts

    def get_conflict_warnings(self) -> list[str]:
        """Return readable warnings for all detected scheduling conflicts."""
        warnings = []
        for first, second in self.detect_conflicts():
            first_pet = self._pet_for_task(first)
            second_pet = self._pet_for_task(second)
            first_name = first_pet.name if first_pet else "Unknown pet"
            second_name = second_pet.name if second_pet else "Unknown pet"
            when = _as_datetime(first.due_date).strftime("%b %d at %I:%M %p")
            warnings.append(
                f"Warning: {first.title} ({first_name}) and {second.title} "
                f"({second_name}) conflict around {when}."
            )
        return warnings

    def _pet_for_task(self, task: Task) -> Pet | None:
        """Find the owner pet that contains a task."""
        return next(
            (pet for pet in self.owner.get_pets() if any(saved is task for saved in pet.get_tasks())),
            None,
        )

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
