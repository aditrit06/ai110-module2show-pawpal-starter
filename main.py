"""A simple example of building and displaying a PawPal+ schedule."""

from datetime import date, datetime

from pawpal_system import Owner, Pet, Scheduler, Task


# Create an owner and two pets.
owner = Owner(owner_id=1, name="Alex")
max_pet = Pet(pet_id=1, name="Max", age=4, breed="Dog")
luna_pet = Pet(pet_id=2, name="Luna", age=3, breed="Cat")
owner.add_pet(max_pet)
owner.add_pet(luna_pet)

# Add tasks out of order to demonstrate sorting. Walk and Luna's checkup overlap.
today = date.today()
walk_max = Task(
    title="Walk",
    due_date=datetime.combine(today, datetime.strptime("10:00 AM", "%I:%M %p").time()),
    priority="Medium",
    duration_minutes=30,
)
feed_max = Task(
    title="Feed",
    due_date=datetime.combine(today, datetime.strptime("8:00 AM", "%I:%M %p").time()),
    priority="High",
    recurrence_frequency="daily",
    duration_minutes=10,
)
feed_luna = Task(
    title="Vet checkup",
    due_date=datetime.combine(today, datetime.strptime("10:15 AM", "%I:%M %p").time()),
    priority="High",
    duration_minutes=45,
)

# Keep each task with the pet it belongs to.
max_pet.add_task(feed_max)
max_pet.add_task(walk_max)
luna_pet.add_task(feed_luna)

# The scheduler reads tasks from all pets belonging to the owner.
scheduler = Scheduler(owner)
sorted_tasks = scheduler.sort_by_time()

print("Today's Schedule")
for task in sorted_tasks:
    # Find which pet owns this task so its name can be included in the display.
    pet_name = "Unknown pet"
    for pet in owner.get_pets():
        if task in pet.get_tasks():
            pet_name = pet.name
            break

    task_time = task.due_date.strftime("%I:%M %p")
    print(f"{task_time} | {pet_name} | {task.title} | Priority: {task.priority}")

print("\nIncomplete tasks for Max")
for task in scheduler.filter_tasks(pet_name="Max", completed=False):
    print(f"{task.title} at {task.due_date.strftime('%I:%M %p')}")

print("\nConflict warnings")
for warning in scheduler.get_conflict_warnings():
    print(warning)

print("\nComplete Max's daily feeding")
next_task = scheduler.mark_task_complete(feed_max)
if next_task:
    print(f"Next occurrence: {next_task.title} on {next_task.due_date:%Y-%m-%d %I:%M %p}")
