# Day 9 : Proof of work

**Date completed:** 2026-10-29 · **Time spent:** 6-7 hrs

## Success criteria

| **Criterion** | **Done?** | **POW** |
| --- | --- | :--- |
| Understands BEE and Learn and explores both | Yes | Key learnings: [BEE and Learn](#bee-and-learn); [Exercise 1](#exercise-1-install-and-explore-bee-and-learn) (BEE: design brief, [PRD](https://github.com/shaswatmishra-work/coe-shaswat/blob/main/smart-ocr-v1-discovery.md) and approved [Phase 1 spec](https://github.com/shaswatmishra-work/coe-shaswat/blob/main/smart-ocr-v1-phase-1-spec.md); Learn: Lesson 1, two quizzes, [script](https://github.com/shaswatmishra-work/coe-shaswat/blob/main/prescription_match.py)) |
| Estimates realistically in AI-first teams | Yes | Key learnings: [What AI speeds up](#what-ai-speeds-up-and-what-it-doesnt); [Exercise 2](#exercise-2-sprint-plan-for-smart-ocr) estimates |
| Slices items into vertical slices | Yes | [Exercise 2](#exercise-2-sprint-plan-for-smart-ocr): Smart OCR slices |
| Keeps review discipline in the Definition of Done | Yes | Key learnings: [Definition of Done](#definition-of-done-when-ai-writes-code); [Exercise 2](#exercise-2-sprint-plan-for-smart-ocr) Definition of Done |
| Explains AI as an amplifier per DORA research | Yes | Key learnings: [DORA](#dora-ai-as-an-amplifier) |
| Knows what to monitor for AI features in production | Yes | Key learnings: [Monitoring](#monitoring-ai-features-in-production) (Smart OCR dashboards) |
| Plans a realistic sprint for an AI feature | Yes | [Exercise 2](#exercise-2-sprint-plan-for-smart-ocr) |

## Key learnings

Some examples come from Visit Health, my last company, an Indian health benefits platform. Members upload prescriptions to order medicines, book lab tests or claim money back, and the details on each prescription have to be typed into our system (we called this digitisation). Doctors used to do this by hand, at about 15 minutes per prescription. I built **Smart OCR**, which reads the prescription with AI and fills in the fields, so the doctor only checks and corrects them. That brought it down to under 2 minutes.

### BEE and Learn

Both are Incubyte plugins for Claude Code. BEE runs spec-driven development: it first judges how big and risky a task is, then takes it through the steps it needs, from spec and architecture to code, tests and review. A small fix gets a light process and a risky feature gets the full one, which is the same lesson I took from Day 4: the spec should be as big as the problem. Learn is built for learning rather than code generation. It builds a project-based course where you write the code yourself, with quizzes along the way. The same repo also has a Discovery plugin that takes an idea through to a PRD and will recommend dropping an idea that should die, which links back to Day 3.

### How engineers use Claude Code

Claude Code reads the whole codebase, edits files, runs commands and tests, and makes commits and pull requests. Teams put their coding standards and review checklists in a CLAUDE.md file that it reads every session, and connect it to tools like Jira through MCP. So the developer's job moves from typing code to describing the change well and checking what comes back.

### What AI speeds up, and what it doesn't

At Visit Health our engineers used Claude. Front-end work got clearly faster, because the AI had the Figma designs as context. Back-end work got faster at first, but then QA kept finding issues and the work went round in loops, so the total time ended up about the same as without AI. Looking back, the cause was the chain: business analysts wrote Jira tickets with AI, developers gave those tickets to AI to write code, and QA became the only real check. For estimates, this means I estimate the review and fixing, not the typing. I only reduce estimates where the AI has full context, like front end from Figma, and I treat QA capacity as the real limit.

### Slicing into vertical slices

The Humanizing Work guide defines a story as a change in system behaviour from the user's point of view. A vertical slice goes through every layer (screen, logic, data) so a user sees something new. Splitting by layer, like "build the database", gives tasks, not stories. A good size is 6 to 10 stories per sprint. The guide lists nine splitting patterns, such as workflow steps, data variations, simple versus complex, defer performance, and a time-boxed spike as a last resort. The idea underneath them all: find the core complexity, list the variations, and build just one variation first. For new, uncertain work, they suggest building one or two slices to learn instead of trying to list every story up front.

### Definition of Done when AI writes code

From my Visit Health experience and the DORA material, review matters more with AI, not less. AI can write a lot of code in one go and can grade its own work, so a separate human check after every small change is what keeps quality. My Definition of Done would require a human-reviewed ticket with acceptance criteria before coding starts, a second developer's review on every pull request, tests that a person has written or checked, and QA against the acceptance criteria.

### DORA: AI as an amplifier

For this section I read the summary of the 2025 report on DORA's website and its companion page on the AI Capabilities Model, and watched Dave Farley's video review. I didn't read the full report, so the figures come from his video.

The report's main finding is that AI acts as an amplifier: it magnifies a team's existing strengths and its existing weaknesses. Teams with strong practices gain more, and teams with weak ones see their problems grow. In Farley's account, the 2024 research found more AI use went with worse stability and throughput. In 2025, about 95% of respondents used AI help and about 80% said it made them more productive, even though many didn't trust its output. So the question has moved from whether to use AI to what needs to surround it.

DORA names seven capabilities that amplify AI's benefits: 

- Clear AI stance

- Healthy data

- AI-accessible internal data

- Strong version control

- Small batches

- User-centric focus

- Quality internal platforms

None of them is a tool. Farley connects them to three basics of programming that AI puts at risk: a precise specification, checking you got what you wanted, and moving in small steps. His example stuck with me: Kent Beck asked an AI to make his test pass and was told 80% of tests now passed, but his own test wasn't one of them. The AI had marked its own homework. That matches what I saw at Visit Health, where vague AI-written tickets became fast, confident and wrong code.

### Monitoring AI features in production

For Smart OCR I saved, for every field on every prescription, the value the AI gave and the value the doctor finally saved. For example, the AI read the symptom as "feverish" and the doctor changed it to "fever". Taking the doctor's value as correct, I measured how closely the two text values matched, as a percentage. That gave me an internal accuracy dashboard by field (for example, the average accuracy of the date across all prescriptions) and by prescription (the average across its fields). A second dashboard tracked cost per prescription, which depended on the number of pages, handwritten versus printed, and how clear the photo was. I also asked the AI for a confidence score with each answer, so I could see whether its confidence matched its real accuracy. Together these covered quality, cost and doctor feedback, since every doctor edit was a piece of feedback. Watching these numbers week by week is how quality drift shows up, for example if a new prescription format starts lowering the accuracy of one field.

## Exercises

### Exercise 1: Install and explore BEE and Learn

I installed both plugins in Claude Code and gave each a task linked to Smart OCR, so I could compare what they produced with my own work. As a product manager I took BEE as far as approved specs and stopped before architecture and code.

#### BEE: /bee:sdd

**Task I gave it:** "Smart OCR v1: on the doctor's digitisation screen, pre-fill date, doctor name and patient name from a printed, single-page prescription. The doctor can edit each field. Save both the AI's value and the doctor's final value for every field." I ran it in an empty folder.

| **Step** | **What happened** |
| --- | --- |
| Scope questions | Where the screen lives (build from scratch), how the prescription arrives (doctor uploads a file), and what to do when the AI isn't confident (always pre-fill). |
| Triage | FEATURE size, HIGH risk, because patient details pass through AI and get stored. Discovery later raised it to EPIC with three phases, which I accepted. |
| Design brief | A design agent asked me about feel, colours, fonts, shapes and device. I approved the brief but asked for a different colour palette and a "Revert to AI value" option on edited fields. |
| Discovery (PRD) | Three rounds of questions: patient data and records, files and success, then follow-ups. It wrote five hypotheses, a success target (at least 80% of fields saved unedited across the first 50+ prescriptions), a safety rule (test data only until the AI provider signs a data agreement under HIPAA), three phases and 11 open questions. |
| Phase 1 spec | Four thin slices (sign in, upload and preview, AI pre-fill, edit and save) with 35 acceptance criteria, plus 6 assumptions it made itself, listed for me to accept or change. |
| Architecture | It proposed a stack and AI providers. I stopped here, as these choices belong to engineering. |

Every step ended with a review gate: BEE would not move on until I marked the document reviewed. Files produced: the design brief, the discovery PRD ([smart-ocr-v1-discovery.md](https://github.com/shaswatmishra-work/coe-shaswat/blob/main/smart-ocr-v1-discovery.md)) and the Phase 1 spec ([smart-ocr-v1-phase-1-spec.md](https://github.com/shaswatmishra-work/coe-shaswat/blob/main/smart-ocr-v1-phase-1-spec.md)).

**My view:** BEE is a strong tool that covers the full development cycle, from requirements and specs to code, tests and review, though I only used it up to specs. It follows what the DORA report recommends: work in small batches, have a clear and shared stance on how AI is used, control the process and leave nothing for the AI to assume, and review after every batch. For someone new to Claude code, it also works like a copilot that teaches you how to do AI-assisted development if yoy want to.

#### Learn

**Task I gave it:** "Python basics to compare AI-extracted prescription fields with doctor-saved values and calculate a match percentage", a small version of my Smart OCR accuracy dashboard.

**What happened:** at first it wrote the whole script and ran it (4 of 6 fields matched, 66.7%). When I said I wanted to learn Python, it switched to teaching: a six-lesson plan ending with me rebuilding the script, and Lesson 1 on variables, text and comparing values, with exercises for me to type. I scored 1 out of 3 on its first prediction quiz. I got "1 tablet" versus "one tablet" and "After food" versus "after-food" wrong, because Python doesn't understand meaning, only characters. I then tried its other commands: /why, /explain, /map, /teach, /speed and /quiz, where I scored 3 out of 3. It saved my notes in [python-lessons.md](https://github.com/shaswatmishra-work/coe-shaswat/blob/main/python-lessons.md) alongside the script, [prescription_match.py](https://github.com/shaswatmishra-work/coe-shaswat/blob/main/prescription_match.py).

**What I learned:** /why compared five ways to decide if two values match and measured them. Text similarity rated "twice a day" versus "thrice a day" as 84% similar, even though that is a dosing error. My Visit Health dashboard used a similarity percentage, which would have given that pair partial credit. In the quiz I reasoned the same way about "5 mg" versus "50 mg": one character apart, but ten times the dose. For dosage fields, an exact match after tidying up spaces and capitals is safer.

**My view:** Learn is a very good learning tool. It teaches with a running example, and you can ask it to explain, go deeper, quiz you, draw a map, slow down or speed up. It feels like a classroom and an internship in one: when you finish the course, you also have a working project.

### Exercise 2: Sprint plan for Smart OCR

**The team** was one Visit Health pod: a tech lead, 2 backend developers, 1 web developer, 1 iOS developer, 1 Android developer, a UX/UI designer and 2 QA. Sprints were two weeks. I count about 9 working days per person per sprint after ceremonies.

**How I sliced it.** Using the guide's core idea: the core complexity is reading prescriptions reliably. The variations are printed or handwritten, one page or several, clear or blurred photos, and many different fields. So the first slice takes one of each: a printed, single-page, clear prescription with only three fields. Every later slice adds one variation.

| **#** | **Slice (what a user can now do)** | **Pattern** | **Estimate (days)** | **Sprint** |
| --- | --- | --- | --- | --- |
| 0 | Spike: test two OCR/AI options on 100 real prescriptions for field accuracy and cost (time-boxed) | Spike | Backend 2, tech lead | 1 |
| 1 | Doctor sees date, doctor name and patient name pre-filled from a printed, single-page prescription, edits them, and both values are saved | Simple/complex, data variations | Backend 4, web 2, QA 3, design 2 | 1 |
| 2 | Medicines and lab tests are pre-filled too (what drives orders) | Data variations | Backend 3, web 1, QA 2 | 1 |
| 3 | I can see accuracy by field and by prescription on an internal dashboard | Workflow steps | Backend 2, QA 1 | 1 |
| 4 | Handwritten prescriptions are read, and low-confidence fields are highlighted for the doctor (behind a feature flag) | Data variations | Backend 4, web 2, design 1, QA 3 | 2 |
| 5 | Multi-page prescriptions are combined; unreadable photos trigger a re-upload request in the app | Data variations | Backend 3, web 1, iOS 1, Android 1, design 1, QA 2 | 2 |
| 6 | I can see cost per prescription by pages, handwritten or printed, and photo quality | Defer performance (cost) | Backend 1, QA 1 | 2 |

**Why** **these estimates are** **realistic.** Web estimates are lower because the AI has the Figma designs. Backend estimates are not reduced, because that is where AI-written code kept coming back from QA. In Sprint 1, backend has 11 of 18 days planned, leaving 7 days (about 40%) for review and rework. QA has spare capacity on paper, but in my experience, it is the real limit once AI is writing the code, so I didn't fill it. The iOS and Android developers are only needed in Sprint 2 and work on other pod items until then. If Sprint 1 goes well, the next items get pulled in rather than planned now, since this is new work and we will learn as we go. Sprint 1 has four slices, because the spike and the first slice carry most of the uncertainty. Once they are done, later slices can be split thinner.

**Definition of Done for every slice:**

1. The ticket and acceptance criteria are reviewed by me before development starts, even if AI helped write them.

2. Another developer reviews every pull request, even when AI wrote the code.

3. Tests are written or checked by a person, not only generated.

4. QA checks the slice against the acceptance criteria on real, redacted prescriptions.

5. The AI value and the doctor's final value are being logged before release, so monitoring works from day one.

6. Handwritten reading (slice 4) stays behind the flag until field accuracy on a set of 100 real prescriptions reaches our 85% target (it was about 70%).

**Comparing my plan with BEE's.** Both start with the thinnest end-to-end slice and save the AI value next to the doctor's value from the first release. BEE's slices were thinner and it added things I had taken for granted, because it was building from scratch: sign-in, a test-data-only rule and deleting files after the AI reads them. It also turned my vague "accuracy" into a target (80% of fields saved unedited across 50+ prescriptions) and listed its own assumptions for me to approve. Mine differed in two ways I would keep: a spike to compare AI providers before building, which BEE left as an open question, and the accuracy dashboard in Sprint 1, where BEE left measurement to Phase 3.

## Reflection

AI made writing tickets and code faster at Visit Health, but it didn't make delivery faster, because the checking just moved to the end. That changes my role. My most valuable work is now making the spec precise before anyone, human or AI, starts building, and making sure every slice has a real check that the AI can't mark itself. I also have to estimate the review and rework, not the typing, and plan monitoring as part of the first slice instead of something added after launch. DORA's amplifier idea put words to what I saw: AI made our good habits faster and our weak ones louder.

## AI use

I used Claude (claude.ai) at set points in my process. The reading, the choice of examples, the exercises and the final decisions were mine:

1. Starting:

   1. I read the 2 articles, summary of DORA 2025, watched a video on the same and went through the readme file of plugins.

   2. I read the day's exercises to understand what I needed to show.

2. Exercise:

   3. I picked the experience from my last company that best fit each exercise, explained the whole project to Claude and how it fits the exercise, and asked whether it was a good example. Based on Claude's response, I either changed the example or continued with it.

   4. I did the exercise myself using the concepts from the readings, then gave it to Claude to polish, asking it to check with me before making any changes, since I own the result.

   5. Once all the exercises were done, I asked Claude to polish each output so the reader can follow what I was thinking while doing the exercise.

   6. I reviewed Claude's output before copying it into my document. For example, Claude suggested how to split Smart OCR into slices, which I checked against how the feature was actually built and the team I had.

3. Theory:

   7. For the theory, I listed every topic I studied. Under each topic, I first copied in the content from the article, then added my own opinion and how I have used it in the past or plan to use it in future.

   8. Once the theory part was done, I asked Claude to polish each section. I reviewed Claude's output before copying it into my document.

4. Claude Code:

   9. Added Incubyte marketplace to my claude, Added plugins from that marketplace

   10. Took some examples and experimented with both of the plugins. (Added .md files of the results in the same repo)

   11. Shared my experience with claude and opinion on both plugins so that it can add it in the final doc

5. Submission:

   12. I reviewed the whole document, made changes where needed, and then submitted it.


