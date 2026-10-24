from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


class Owner:
	def __init__(self, owner_id: int, name: str) -> None:
		self.owner_id: int = owner_id
		self.name: str = name
		self.pets: list[Pet] = []

	def add_pet(self, pet: Pet) -> None:
		pass

	def get_pets(self) -> list[Pet]:
		pass


@dataclass
class Pet:
	pet_id: int
	name: str
	age: int
	breed: str
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		pass

	def get_tasks(self) -> list[Task]:
		pass


@dataclass
class Task:
	title: str
	due_date: date
	priority: str
	recurring: bool = False
	completed: bool = False

	def mark_complete(self) -> None:
		pass


class Scheduler:
	def __init__(self) -> None:
		self.tasks: list[Task] = []

	def add_task(self, task: Task) -> None:
		pass

	def sort_tasks(self) -> None:
		pass

	def detect_conflicts(self) -> None:
		pass

	def get_upcoming_tasks(self) -> None:
		pass
