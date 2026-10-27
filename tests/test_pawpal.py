from datetime import date

from pawpal_system import Pet, Task


def test_task_can_be_marked_complete():
    task = Task(title="Feed", due_date=date.today(), priority="High")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_pet_can_add_task():
    pet = Pet(pet_id=1, name="Max", age=4, breed="Dog")
    initial_task_count = len(pet.get_tasks())
    task = Task(title="Walk", due_date=date.today(), priority="Medium")

    pet.add_task(task)

    assert len(pet.get_tasks()) == initial_task_count + 1
