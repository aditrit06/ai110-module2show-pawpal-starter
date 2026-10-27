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
st.subheader("Your Pets")

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
st.subheader("Schedule a Task")

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
                duration_minutes=int(duration),
            )
            selected_pet.add_task(task)
            st.success(f"Added {task.title} for {selected_pet.name}!")
else:
    st.caption("Add a pet to enable task scheduling.")

st.divider()
st.subheader("Today's Schedule")

scheduler = Scheduler(owner)
sorted_tasks = scheduler.sort_tasks()
if sorted_tasks:
    for task in sorted_tasks:
        task_pet = next(
            pet for pet in owner.get_pets() if any(saved_task is task for saved_task in pet.get_tasks())
        )
        if isinstance(task.due_date, datetime):
            task_time_text = task.due_date.strftime("%b %d, %I:%M %p")
        else:
            task_time_text = task.due_date.strftime("%b %d")
        st.write(
            f"{task_time_text} | **{task_pet.name}** | {task.title} "
            f"| Priority: {task.priority}"
        )
else:
    st.info("No tasks scheduled yet.")
