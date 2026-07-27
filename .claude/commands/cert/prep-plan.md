---
description: Build a study plan for one certification, shaped by your time, experience, and target date
argument-hint: [certification] [hours per week] [target date]
---

Build a preparation plan for the certification in `$ARGUMENTS`.

## Gather what is missing

Ask only for what was not supplied, in one message rather than one question at a time: the certification, hours available per week, target exam date if any, current experience with the technologies in the blueprint, and whether a `/cert:diagnostic` has been run. If a diagnostic was run in this session, use its domain scores instead of asking about experience.

## Build

1. Read the certification's `README.md` (blueprint and weights), `notes.md` (what matters within each domain), and `guide/study-strategy.md` (the method and per-exam emphasis).
2. Read `guide/courses.md` for the official courses that teach each area, and `guide/resources.md` for documentation and videos.

Produce a plan with:

- **Scope.** The blueprint as a checklist of objectives, ordered by exam weight, with the candidate's confidence marked where known.
- **Sequence.** Which courses, documentation, and engineering articles to work through, and in what order. Weight time by domain percentage, not by personal interest: name explicitly where the heaviest domains are.
- **Build task.** The one thing to build with their own hands, taken from the certification's preparation section. This is not optional; every official guide asks for it.
- **Checkpoints.** Where in the schedule to run `/cert:drill` and `/cert:mock`, and what score to expect at each before proceeding.
- **Fit to the calendar.** Translate all of the above into their stated hours per week and target date. If the date is not achievable at that pace, say so plainly and give the two options: move the date or raise the hours.

Close by offering `/cert:weekly-plan` for the next week in detail.
