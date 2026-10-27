# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
I designed PawPal+ using four main classes: Owner, Pet, Task, and Scheduler. The Owner class stores information about pet owners and manages their pets. The Pet class stores details about each pet and its care tasks. The Task class represents activities like feeding, walking, medications, and appointments, including their scheduled times and priorities. Finally, the Scheduler class organizes tasks, detects scheduling conflicts, and helps manage upcoming activities.

I chose these four classes because they separate different responsibilities and make the application easier to understand and maintain. I also created a UML diagram to visualize how the classes connect before implementing the actual code.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
After reviewing my initial design with AI, I identified a few improvements. The original UML diagram was missing some class details and contained unnecessary placeholder classes. I also realized that tasks needed specific start times and durations to make scheduling conflict detection possible.

Another improvement was making the relationship between pets and tasks clearer. I decided that each Pet would be the source of truth for its tasks. The Owner can gather them with `get_all_tasks()`, and the Scheduler keeps a refreshed working view rather than owning a second, independent copy. I also added a recurrence frequency so tasks could support daily and weekly scheduling.

These changes made my design more organized and gave the scheduling algorithms a clear way to access tasks across pets. AI helped me think through the design, but I checked that the final structure stayed simple and matched how I wanted the data to be owned.

**Three Core Actions:**

1. **Add and manage pets:** Users should be able to add their pets to the system and store basic information such as their name, age, breed, and owner.

2. **Schedule pet care tasks:** Users should be able to create tasks for their pets, such as feeding, walking, giving medication, or scheduling vet appointments. Each task should have a date, time, and priority.

3. **View and organize daily tasks:** Users should be able to view their pets' upcoming tasks in an organized schedule. The system should sort tasks by time and priority, detect scheduling conflicts, and help manage recurring tasks.

---

## 2. Scheduling Logic and Tradeoffs

### 2b. Tradeoffs

Conflict detection compares scheduled start times and task durations. This catches exact-time conflicts and overlapping appointments, but it assumes each task's duration is accurate and does not account for travel time or setup between activities. Keeping the check focused on time makes the warning easy to understand while leaving those real-world details for a later version.

During implementation, I used AI to help turn my UML design into working Python code. AI helped me implement the Owner, Pet, Task, and Scheduler classes and suggested how the Scheduler could retrieve tasks from multiple pets using the Owner's `get_all_tasks()` method.

One suggestion I accepted was keeping each pet's tasks in the Pet class. The Scheduler can gather them through the Owner, so the Pet remains the source of truth while the Scheduler uses a refreshed view. I also used AI to help create a demo script and tests. I chose to keep the implementation beginner-friendly rather than adding unnecessary complexity.

To verify the AI-assisted code, I ran the CLI demo and checked that it displayed tasks from both pets in chronological order, showed a conflict, and created the next daily occurrence. The test file now contains eight tests covering task completion, adding tasks, sorting, filtering, daily recurrence, conflicts, and empty schedules; the recorded pytest run passed all eight.

This experience helped me understand that AI can make coding faster, but it is still important to review the generated code and test it. I learned that successful AI collaboration involves giving clear instructions, understanding the suggestions, and verifying that the final implementation meets the project requirements.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used my AI coding assistant throughout the project. I started by brainstorming the Owner, Pet, Task, and Scheduler classes and reviewing how they should relate in the UML. I then used it to help implement the object-oriented classes, improve the sorting, filtering, recurrence, and conflict-checking algorithms, connect those methods to the Streamlit interface, and create tests. I got the most useful responses when I asked the assistant to inspect the actual files and method signatures, make a focused change, or explain an algorithm in plain language.

I also found it helpful to review multiple files together. For example, comparing the UI with the backend and tests helped me check that the app was calling existing Scheduler methods and that the documented behavior matched what the code actually did. The assistant also helped me think of edge cases such as overlapping task durations, tasks with identical start times, empty schedules, and completing a recurring task.

To stay organized, I separated chats by type of work: planning and UML, implementation, scheduling algorithms, testing, and final project polish. Keeping each conversation focused made it easier for me to follow the current question and return to earlier decisions when I needed them.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I do not have a specific rejected suggestion that I can accurately describe, so I do not want to invent one. A real design decision I made was to keep task ownership in `Pet`: each pet stores its own tasks, `Owner.get_all_tasks()` gathers them, and the Scheduler refreshes its task view from the Owner. I checked this against the Python implementation and the final UML. I also reviewed generated code and explanations against the existing methods and tests instead of assuming they were correct. I see my role as the lead architect: AI can help draft options and code, but I am responsible for the design, checking behavior, running tests, and choosing what belongs in the final project.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

My tests check that a task can be marked complete, a pet can store a task, the Scheduler sorts tasks by time, and filters can select tasks by pet and completion status. They also check that completing a daily task creates its next occurrence, overlapping tasks and identical start times create conflict warnings, and an empty schedule is handled safely. These tests matter because they check the main user-facing scheduling behavior as well as cases where there are no tasks or the schedule has a conflict.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident in the behaviors covered by the eight tests and the CLI example, but I would not assume that this proves every schedule will work correctly. If I had more time, I would add tests for weekly recurrence, tasks with the same start time but different priorities, and date-only tasks. I would also check what should happen when completing a non-recurring task and when several recurring occurrences build up.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied that the project grew from a UML design into a working backend and a Streamlit interface without losing the clear roles of the four classes. The schedule can bring together tasks for different pets, and the demo and tests make the behavior easier to see and check.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

In another iteration, I would add ways to edit or remove pets and tasks, and I would test more recurrence cases, especially weekly schedules. I would also think more about real-life scheduling details like travel time between appointments, since the current conflict check only uses each task's scheduled time and duration.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that clear ownership of data makes the rest of a system easier to reason about: pets store their tasks, the owner gathers them, and the scheduler organizes that gathered view. I also learned that working with AI is most useful when I give it specific context and then verify its suggestions. I am still responsible for understanding and standing behind the design and code I submit.

