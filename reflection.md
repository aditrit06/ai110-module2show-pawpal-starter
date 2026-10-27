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

Another improvement was making the relationship between pets and tasks clearer. I decided to use the Pet class as the main place to store tasks so that the Scheduler wouldn't have to maintain a separate duplicate list. I also added a recurrence frequency to make it easier to support daily and weekly tasks in the future.

These changes helped make my design more organized and prepared it for the scheduling algorithms I'll implement later. AI helped identify potential problems, but I focused on keeping the design simple and manageable.

**Three Core Actions:**

1. **Add and manage pets:** Users should be able to add their pets to the system and store basic information such as their name, age, breed, and owner.

2. **Schedule pet care tasks:** Users should be able to create tasks for their pets, such as feeding, walking, giving medication, or scheduling vet appointments. Each task should have a date, time, and priority.

3. **View and organize daily tasks:** Users should be able to view their pets' upcoming tasks in an organized schedule. The system should sort tasks by time and priority, detect scheduling conflicts, and help manage recurring tasks.

---

## 2. Scheduling Logic and Tradeoffs

### 2b. Tradeoffs

Conflict detection compares scheduled start times and task durations. This catches exact-time conflicts and overlapping appointments, but it assumes each task's duration is accurate and does not account for travel time or setup between activities. Keeping the check focused on time makes the warning easy to understand while leaving those real-world details for a later version.

During Phase 2, I used AI to help turn my UML design into working Python code. AI helped me implement the Owner, Pet, Task, and Scheduler classes and suggested how the Scheduler could retrieve tasks from multiple pets using the Owner's `get_all_tasks()` method.

One suggestion I accepted was keeping each pet's tasks in the Pet class instead of maintaining duplicate task lists. This made the design simpler and helped keep the data organized. I also used AI to generate a demo script and two pytest tests. I chose to keep the implementation beginner-friendly rather than adding unnecessary complexity.

To verify the AI-generated code, I ran `python main.py` and checked that the schedule displayed three tasks from two different pets in chronological order. I also ran `python -m pytest`, and both tests passed successfully.

This experience helped me understand that AI can make coding faster, but it is still important to review the generated code and test it. I learned that successful AI collaboration involves giving clear instructions, understanding the suggestions, and verifying that the final implementation meets the project requirements.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

