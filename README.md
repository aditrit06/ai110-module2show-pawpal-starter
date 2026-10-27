# PawPal+ (Module 2 Project)

PawPal+ is a Python-based pet care management system designed to help pet owners organize their pets' daily routines, including feeding, walking, medications, grooming, and appointments.

The application uses object-oriented programming (OOP) to manage multiple pets, track their tasks, and organize daily schedules based on scheduled times and priorities.

## 🐾 Scenario

A busy pet owner needs help staying consistent with pet care. PawPal+ is designed to help owners:

- Track daily pet care activities such as feeding, walking, medications, and grooming.
- Organize tasks based on scheduled times and priorities.
- Manage care routines for multiple pets.
- Track completed and upcoming tasks.
- Identify potential scheduling conflicts.
- Support recurring activities such as daily feedings and weekly grooming.

The goal is to create a simple and organized system that makes pet care easier to manage.

## 🎯 Features

PawPal+ includes the following working features:

- Add pets and view the pets in the owner's list.
- Schedule care tasks for a selected pet, including a title, date, time, duration, priority, and recurrence choice.
- Display scheduled tasks in chronological order, with priority used to order tasks that share a time.
- Filter the schedule by pet and completion status (all, completed, or incomplete).
- Set a task to repeat daily or weekly. Completing a recurring task creates its next occurrence.
- Detect tasks with the same start time or overlapping durations and show readable conflict warnings.
- Mark tasks complete from the Streamlit schedule.
- Run a command-line demonstration and automated tests for the scheduling backend.

## ⚙️ Getting Started

### Setup

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run the CLI Demo

To run the demonstration script:

```bash
python main.py
```

This script creates an owner with two pets, adds three care tasks, and demonstrates chronological sorting, filtering, conflict warnings, and daily recurrence.

### Run the Tests

To run the automated tests:

```bash
python -m pytest
```

## 🏗️ System Design

PawPal+ was designed using a modular object-oriented architecture consisting of four main classes.

### 1. Owner

The Owner class stores information about the pet owner and manages multiple pets.

Responsibilities:

- Store owner information.
- Add and retrieve pets.
- Collect tasks from all pets using `get_all_tasks()`.

### 2. Pet

The Pet class represents an individual pet and stores its care tasks.

Responsibilities:

- Store pet information such as name, age, and breed.
- Add new care tasks.
- Retrieve the pet's scheduled tasks.

### 3. Task

The Task class represents a single pet care activity.

Responsibilities:

- Store task information such as title, scheduled time, duration, and priority.
- Track completion status.
- Store recurrence information.
- Mark tasks as completed using `mark_complete()`.

### 4. Scheduler

The Scheduler class is responsible for organizing pet care tasks.

Responsibilities:

- Retrieve tasks from multiple pets through the Owner class.
- Sort tasks by scheduled time.
- Provide methods for detecting scheduling conflicts.
- Retrieve upcoming tasks.

### UML Diagram

The final class architecture is documented in [diagrams/uml_final.mmd](diagrams/uml_final.mmd). The original draft remains available at [diagrams/uml_draft.mmd](diagrams/uml_draft.mmd) to show how the design evolved.

The diagram shows the Owner, Pet, Task, and Scheduler classes, their key attributes and methods, and their relationships.

## 💻 Implementation Summary

I implemented the core PawPal+ backend using Python and object-oriented programming.

The application separates responsibilities across four classes to make the code easier to understand, maintain, and expand.

The Owner class manages multiple pets, while each Pet stores its individual care tasks. The Task class represents scheduled activities, and the Scheduler retrieves and organizes tasks across pets.

I followed a CLI-first development approach, which allowed me to implement and verify the backend before connecting it to the Streamlit user interface. The Streamlit interface now uses the backend classes to add pets, schedule tasks, filter and display the schedule, show conflict warnings, and complete tasks.

To demonstrate the implementation, I created a `main.py` script containing:

- One pet owner.
- Two pets named Max and Luna.
- Three care tasks with different scheduled times.
- A scheduler that displays tasks from both pets in chronological order.

I also created automated tests using pytest to verify important functionality.

## 🧪 Testing PawPal+

The eight automated tests in `tests/test_pawpal.py` check that PawPal+ handles its main task and scheduling features:

- **Marking tasks complete:** Checks that a task changes from incomplete to complete.
- **Adding tasks to pets:** Checks that a pet can store a new task.
- **Sorting tasks chronologically:** Checks that tasks are returned in time order, even when added out of order.
- **Filtering by pet and completion status:** Checks that results include only tasks matching the requested pet and completed or incomplete status.
- **Creating the next occurrence of daily tasks:** Checks that completing a daily task marks the original complete and creates a task for the following day.
- **Detecting overlapping tasks:** Checks that tasks with overlapping durations produce a readable warning.
- **Handling empty schedules:** Checks that sorting and filtering return empty lists and conflict detection finds no conflicts when there are no tasks.
- **Detecting identical start times:** Checks that tasks scheduled for the same time conflict, including when both tasks have zero duration.

### Activate the Virtual Environment and Run the Tests

From the project folder, activate the virtual environment and run pytest:

```bash
source .venv/bin/activate
python -m pytest
```

### Successful Test Output

```text
============================= test session starts ==============================
platform darwin -- Python 3.13.14, pytest-9.1.1
rootdir: /Users/aditritangeti/ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 8 items

tests/test_pawpal.py ........                                            [100%]

============================== 8 passed in 0.01s ===============================
```

### Confidence Level

⭐⭐⭐⭐☆ (4/5)

The system passed its automated tests and handles important edge cases. More testing would be needed before using it in production.

## 📐 Smarter Scheduling

PawPal+ can sort and filter tasks, detect conflicts, and create the next occurrence of a recurring task.

| Feature | Method(s) | Description |
|---|---|---|
| Task sorting | `Scheduler.sort_by_time()` and `Scheduler.sort_tasks()` | Orders tasks by scheduled date and time; `sort_tasks()` also uses priority to break ties. |
| Filtering | `Scheduler.filter_tasks(pet_name=..., completed=...)` | Selects tasks by pet name, completion status, or both. `Scheduler.get_upcoming_tasks()` returns incomplete tasks scheduled now or later. |
| Conflict detection | `Scheduler.detect_conflicts()` and `Scheduler.get_conflict_warnings()` | Finds tasks with the same start time or overlapping durations and returns readable warnings. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Completing a daily or weekly task creates its next instance one or seven days later, preserving the scheduled time, priority, and duration. |

The CLI demonstration adds tasks out of order, filters incomplete tasks for one pet, prints conflict warnings, and completes a daily task to show its next occurrence.

## Demo Walkthrough

### Launch the Streamlit app

From the project folder, activate your virtual environment and start the app:

```bash
source .venv/bin/activate
streamlit run app.py
```

The app opens in your browser. Pet and task data is kept in Streamlit session state while you use the app.

### Try a Max and Luna workflow

1. In **Your Pets**, add Max (a dog) and Luna (a cat). The pet list shows each pet after it is added.
2. In **Schedule a Task**, choose Max and add a daily feeding task for 8:00 AM. Add a walk for Max at 10:00 AM, then choose Luna and schedule a vet checkup at 10:15 AM. Set a duration and priority for each task.
3. In **Care Schedule**, view the tasks in date and time order. When tasks share a scheduled time, priority determines their order.
4. Use **Filter by pet** to show Max or Luna's tasks. Use **Filter by completion** to show all tasks, only completed tasks, or only incomplete tasks. The filters can be combined.
5. When two tasks start together or their durations overlap, **Schedule Conflicts** displays a warning naming the tasks, pets, and conflict time. In this example, Max's 10:00 AM walk overlaps Luna's 10:15 AM checkup.
6. Press **Complete** beside Max's daily feeding. The app confirms completion and shows the next occurrence for the following day at the same time. Weekly tasks work the same way, with the next occurrence seven days later.

### Run the command-line demonstration

The CLI example demonstrates backend sorting, filtering, conflict warnings, and daily recurring-task completion. Run it with:

```bash
python main.py
```

The following is the actual output from `python3 main.py` in this project environment:

```text
Today's Schedule
08:00 AM | Max | Feed | Priority: High
10:00 AM | Max | Walk | Priority: Medium
10:15 AM | Luna | Vet checkup | Priority: High

Incomplete tasks for Max
Feed at 08:00 AM
Walk at 10:00 AM

Conflict warnings
Warning: Walk (Max) and Vet checkup (Luna) conflict around Oct 27 at 10:00 AM.

Complete Max's daily feeding
Next occurrence: Feed on 2026-10-28 08:00 AM
```

## 🤖 AI Collaboration

AI was used throughout the design and implementation process to assist with planning, generating code, and reviewing the application structure.

During the design phase, AI helped generate the UML class diagram and identify relationships between the Owner, Pet, Task, and Scheduler classes.

After reviewing the initial design, AI suggested improvements such as adding more detailed scheduling information, clarifying the relationship between pets and tasks, and avoiding unnecessary duplication of task data.

During implementation, AI assisted with generating Python class methods, creating the CLI demonstration, writing automated tests, and adding documentation.

I reviewed these suggestions and focused on keeping the application beginner-friendly while still meeting the project requirements.

To verify the AI-assisted code, I ran the CLI demonstration and automated tests. The CLI displayed tasks from both pets, and the eight pytest tests passed.

This process helped me understand how AI can speed up development while still requiring human review, testing, and decision-making.

## 🚀 Future Improvements

Future improvements for PawPal+ include:

- Allowing users to edit or remove pets and tasks.
- Improving scheduling algorithms to account for available time and priorities.
- Providing more detail about why a scheduling conflict was detected.
- Adding more automated tests for weekly recurrence and multi-pet behavior.

## 📁 Project Structure

```text
ai110-module2show-pawpal-starter/
├── diagrams/
│   ├── uml_draft.mmd
│   └── uml_final.mmd
├── tests/
│   └── test_pawpal.py
├── pawpal_system.py
├── main.py
├── app.py
├── README.md
├── reflection.md
└── requirements.txt
```

## ✅ Project Progress

**Phase 1: System Design**

- Identified core application requirements.
- Designed the main classes and relationships.
- Created a Mermaid UML diagram.
- Generated Python class skeletons.
- Reviewed the design with AI.

**Phase 2: Core Implementation**

- Implemented the four main Python classes.
- Created a CLI demonstration script.
- Verified scheduling output across multiple pets.
- Created eight automated pytest tests.
- Verified that all eight tests passed.
- Documented the implementation and sample output.

**Phase 4: Smart Scheduling**

- Added chronological sorting and task filters.
- Added daily and weekly recurring-task completion.
- Added overlapping-task conflict detection and readable warnings.

**Phase 6: Streamlit UI and Documentation**

- Connected the scheduling features to the Streamlit interface.
- Added the final UML diagram and polished this project manual.

**Next Steps**

Continue improving the scheduling experience and expand automated testing.
