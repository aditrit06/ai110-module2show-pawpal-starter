from datetime import date, datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_scheduler_sorts_tasks_chronologically():
    """Tasks come back in time order even when added in reverse order."""
    owner = Owner(owner_id=1, name="Alex")
    pet = Pet(pet_id=1, name="Max", age=4, breed="Dog")
    owner.add_pet(pet)
    late_task = Task("Evening walk", datetime(2026, 5, 1, 18, 0), "Low")
    early_task = Task("Breakfast", datetime(2026, 5, 1, 8, 0), "High")
    pet.add_task(late_task)
    pet.add_task(early_task)

    scheduler = Scheduler(owner)

    # The earliest task should be first, despite being added second.
    assert scheduler.sort_by_time() == [early_task, late_task]


def test_scheduler_filters_tasks_by_pet_and_completion():
    """Filters can narrow tasks by both their pet and completion status."""
    owner = Owner(owner_id=1, name="Alex")
    max_pet = Pet(pet_id=1, name="Max", age=4, breed="Dog")
    luna_pet = Pet(pet_id=2, name="Luna", age=3, breed="Cat")
    owner.add_pet(max_pet)
    owner.add_pet(luna_pet)
    max_feed = Task("Feed", date.today(), "High")
    max_walk = Task("Walk", date.today(), "Medium")
    luna_feed = Task("Feed", date.today(), "High")
    max_walk.mark_complete()
    max_pet.add_task(max_feed)
    max_pet.add_task(max_walk)
    luna_pet.add_task(luna_feed)

    scheduler = Scheduler(owner)

    # Asking for incomplete Max tasks excludes both Max's completed walk and Luna's task.
    assert scheduler.filter_tasks(pet_name="Max", completed=False) == [max_feed]
    assert scheduler.filter_tasks(completed=True) == [max_walk]


def test_completing_daily_task_creates_next_day_task():
    """Completing a daily task adds the same task for the following day."""
    owner = Owner(owner_id=1, name="Alex")
    pet = Pet(pet_id=1, name="Max", age=4, breed="Dog")
    owner.add_pet(pet)
    today = datetime(2026, 5, 1, 8, 30)
    task = Task("Medicine", today, "High", recurrence_frequency="daily")
    pet.add_task(task)

    next_task = Scheduler(owner).mark_task_complete(task)

    # The original is completed and the pet receives a new instance one day later.
    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task in pet.get_tasks()


def test_overlapping_tasks_produce_conflict_warning():
    """Overlapping task durations are reported as a readable warning."""
    owner = Owner(owner_id=1, name="Alex")
    pet = Pet(pet_id=1, name="Max", age=4, breed="Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", datetime(2026, 5, 1, 10, 0), "Medium", duration_minutes=30))
    pet.add_task(Task("Groom", datetime(2026, 5, 1, 10, 15), "Low", duration_minutes=30))

    warnings = Scheduler(owner).get_conflict_warnings()

    # A readable warning names both conflicting tasks.
    assert len(warnings) == 1
    assert "Walk" in warnings[0]
    assert "Groom" in warnings[0]
