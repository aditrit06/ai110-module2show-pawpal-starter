import streamlit as st
from datetime import datetime

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Keep the same owner and its pets and tasks across Streamlit reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id=1, name="Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, a pet care planning assistant. Add your pets and schedule
care tasks for them below.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** helps pet owners plan care tasks for their pets based on time,
priority, and preferences.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, the system represents pets, owners, and care tasks, then organizes
those tasks into a daily schedule.
"""
    )

st.divider()
st.header("1. Your Pets")
st.caption("Add the pets whose care you want to organize.")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Age", min_value=0, max_value=100, value=1)
    submitted_pet = st.form_submit_button("Add Pet")

if submitted_pet:
    duplicate_pet = any(
        pet.name.casefold() == pet_name.strip().casefold()
        and pet.breed.casefold() == species.casefold()
        for pet in owner.get_pets()
    )
    if not pet_name.strip():
        st.error("Please enter a pet name.")
    elif duplicate_pet:
        st.info(f"{pet_name.strip()} is already in your pet list.")
    else:
        next_pet_id = max((pet.pet_id for pet in owner.get_pets()), default=0) + 1
        pet = Pet(
            pet_id=next_pet_id,
            name=pet_name.strip(),
            age=int(pet_age),
            breed=species,
        )
        owner.add_pet(pet)
        st.success(f"Added {pet.name}!")

pets = owner.get_pets()
if pets:
    for pet in pets:
        st.write(f"**{pet.name}** — {pet.breed}, age {pet.age}")
else:
    st.info("Add a pet before scheduling a task.")

st.divider()
st.header("2. Schedule a Task")
st.caption("Choose a pet, set a date and time, and add a care task.")

if pets:
    pet_choices = {pet.pet_id: pet for pet in pets}
    with st.form("schedule_task_form"):
        selected_pet_id = st.selectbox(
            "Choose a pet",
            options=list(pet_choices),
            format_func=lambda pet_id: pet_choices[pet_id].name,
        )
        task_title = st.text_input("Task title", value="Morning walk")
        task_date = st.date_input("Scheduled date", value=datetime.today().date())
        task_time = st.time_input("Scheduled time", value=datetime.strptime("8:00 AM", "%I:%M %p").time())
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        recurrence = st.selectbox(
            "Repeat",
            ["none", "daily", "weekly"],
            format_func=lambda frequency: {
                "none": "Does not repeat",
                "daily": "Daily",
                "weekly": "Weekly",
            }[frequency],
        )
        submitted_task = st.form_submit_button("Add Task")

    if submitted_task:
        if not task_title.strip():
            st.error("Please enter a task title.")
        else:
            selected_pet = pet_choices[selected_pet_id]
            task = Task(
                title=task_title.strip(),
                due_date=datetime.combine(task_date, task_time),
                priority=priority,
                recurrence_frequency=recurrence,
                duration_minutes=int(duration),
            )
            selected_pet.add_task(task)
            st.success(f"Added {task.title} for {selected_pet.name}!")
else:
    st.caption("Add a pet to enable task scheduling.")

st.divider()
st.header("3. Care Schedule")
st.caption("Review upcoming care, narrow the list with filters, and mark tasks complete.")

scheduler = Scheduler(owner)
all_sorted_tasks = scheduler.sort_tasks()
pet_filter, status_filter = st.columns(2)
with pet_filter:
    selected_pet_name = st.selectbox(
        "Filter by pet",
        options=["All Pets", *[pet.name for pet in pets]],
    )
with status_filter:
    selected_status = st.selectbox(
        "Filter by completion",
        options=["All", "Completed", "Incomplete"],
    )

filtered_tasks = scheduler.filter_tasks(
    pet_name=None if selected_pet_name == "All Pets" else selected_pet_name,
    completed={"All": None, "Completed": True, "Incomplete": False}[selected_status],
)
# Keep the ordering from the Scheduler's main sorting method after applying filters.
filtered_task_ids = {id(task) for task in filtered_tasks}
visible_tasks = [task for task in all_sorted_tasks if id(task) in filtered_task_ids]

st.subheader("Scheduled Tasks")
if visible_tasks:
    task_pets = {
        id(task): pet
        for pet in pets
        for task in pet.get_tasks()
    }
    table_rows = []
    for task in visible_tasks:
        task_pet = task_pets.get(id(task))
        scheduled_at = task.due_date
        table_rows.append(
            {
                "Date and time": scheduled_at.strftime("%b %d, %Y %I:%M %p"),
                "Pet": task_pet.name if task_pet else "Unknown pet",
                "Task": task.title,
                "Priority": task.priority.title(),
                "Status": "Completed" if task.completed else "Incomplete",
                "Repeats": task.recurrence_frequency.title(),
            }
        )
    st.dataframe(table_rows, use_container_width=True, hide_index=True)

    st.subheader("Mark a Task Complete")
    incomplete_tasks = [task for task in visible_tasks if not task.completed]
    if incomplete_tasks:
        for index, task in enumerate(incomplete_tasks):
            task_pet = task_pets.get(id(task))
            due_text = task.due_date.strftime("%b %d, %Y at %I:%M %p")
            action_col, button_col = st.columns([4, 1])
            with action_col:
                st.write(f"**{task.title}** for {task_pet.name if task_pet else 'Unknown pet'} — {due_text}")
            with button_col:
                if st.button("Complete", key=f"complete_task_{id(task)}_{index}"):
                    next_task = scheduler.mark_task_complete(task)
                    st.success(f"Marked {task.title} complete.")
                    if next_task is not None:
                        st.info(f"Next occurrence scheduled for {next_task.due_date:%b %d, %Y at %I:%M %p}.")

    else:
        st.info("There are no incomplete tasks in this view.")
else:
    st.info("No tasks match these filters yet. Add a task or choose different filters.")

st.subheader("Schedule Conflicts")
conflict_warnings = scheduler.get_conflict_warnings()
if conflict_warnings:
    for warning in conflict_warnings:
        st.warning(warning)
else:
    st.success("No scheduling conflicts found.")
