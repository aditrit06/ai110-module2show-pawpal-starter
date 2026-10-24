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

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

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
