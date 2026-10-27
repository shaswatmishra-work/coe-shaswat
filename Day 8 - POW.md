**Day 8 : Responsible AI & Trust by Design**

**Date completed:** 2026-10-23 · **Time spent:** 4 to 5 hours

**Success criteria**

| **Criterion (copied from the planner)** | **Done?** | **Evidence** |
| --- | --- | --- |
| Knows when to keep a human in the loop | Yes | Key learnings: When to keep a human in the loop |
| Designs against rubber-stamping | Yes | Exercise 2: redesigned FWA review flow |
| Designs for provenance | Yes | Key learnings: Provenance; Exercise 2, step 2 |
| Understands hallucination and bias guardrails | Yes | Key learnings: Hallucination and bias |
| Understands privacy and risk in AI products | Yes | Key learnings: Privacy and risk |
| Sets honest client expectations | Yes | Key learnings: Client expectations |
| Reviews a feature against interaction guidelines | Yes | Exercise 1 |
**Key learnings**

Some examples here come from Visit Health, my last company. It is an Indian health benefits platform where members claim back money spent on doctor visits, medicines and lab tests, and a doctor reviews every claim before it is paid. The main example is FWA (fraud, waste and abuse) detection, which I led. It checks each claim with rules and AI, gives it a risk level (Low, Medium, High or Critical) and shows the doctor why before they decide.

**When to keep a human in the loop**

The PAIR Guidebook's point is that people shouldn't trust AI fully, because it works on probabilities. They should know when to rely on it and when to use their own judgement. NIST adds that the human's role should be decided on purpose, not left to chance. My rule of thumb: keep a person in the loop if a mistake costs someone money, health or reputation, if it is hard to undo, or if we haven't measured how accurate the AI is. FWA ticks all three, so the AI only flags and a doctor decides. Sorting support emails is different. If it gets one wrong, someone moves the email, so it can run on its own.

**Designing against rubber-stamping**

If the reviewer just clicks approve, the human check is only for show. NIST notes that people often see AI as more objective than a person, which is what makes clicking through so easy. What helps is telling the reviewer the AI is sometimes wrong, making them look at the actual evidence instead of ticking a box, making it easy to disagree, and tracking how often they overrule the AI. If someone never disagrees, I would want to look closer. At Visit Health, doctors marked each flag as correct, incorrect or "can't say", which also gave us data to improve the flags.

**Provenance**

Provenance means showing where an answer came from so someone can check it. Anthropic's guide on hallucinations suggests asking the model to pull exact quotes first and to drop any claim it can't back with a quote. In FWA the doctor saw which flags fired, the threshold for that member's group and how far it was crossed, the member's last 10 claims and a price comparison. Every flag was also logged with a timestamp.

**Hallucination and bias**

To cut down made-up answers, Anthropic suggests letting the model say "I don't know", keeping it to the documents it was given, and running the same prompt a few times to see if the answers agree. The guide is clear that this lowers the risk but doesn't remove it.

NIST's point on bias is that it can creep in without anyone meaning it to. I could find it in our own system. A physiotherapy rule flagged members under 31 partly because of their age. Thresholds built from past claims can repeat old patterns. And a doctor who sees "High" tends to read the claim looking for fraud. Two things helped. Thresholds were set separately for children, adults and older people, for long-term and short-term illness, and by gender, and members with long-term illnesses got a lower score so they weren't flagged just for needing more care. I also compared flag rates across groups by hand and got thresholds changed when a group was flagged too often. The plan was to automate that check.

**Privacy and risk**

NIST's framework is long, but the core is four functions: Govern (who owns the risk), Map (who is affected), Measure (test and monitor) and Manage (act on what you find, including switching the system off). Two things stood out for health data. AI can reveal private details by combining data, so it is safer to collect less. In FWA, employers' HR teams only saw overall numbers, never individual claims, because of India's DPDP law. And a third-party model is a risk in itself. We ran on Gemini, so a change on Google's side could change our results without us touching anything.

**Client expectations**

NIST says trying to remove all risk is counterproductive. Agree what is acceptable and be open about what remains. If I were presenting FWA to an insurer again, I would say it flags risky claims and explains why, a doctor makes every decision, it cut fraud, misuse and manual review time by about 60%, and roughly 1 in 7 flags turns out to be a genuine claim. I would also say plainly that it won't catch every new trick, and offer a monthly report on flags, overrides and appeals. I would avoid lines like "detects fraud with X% accuracy".

**Exercises**

Both exercises use the FWA review screen. FWA runs many flags, each a check with its own threshold, grouped into four AI checks (document tampering, inflated bills, unusual member behaviour, unusual clinic or lab behaviour). A flag only fires when its threshold is crossed. When a claim is flagged, the doctor sees a pop-up with the risk level and the main reasons, and ticks "I have reviewed the FWA profile" to continue. A side panel shows each flag with the threshold and how far it was crossed, the member's last 10 claims and any price comparison. The doctor marks each flag correct, incorrect or "can't say", then makes a decision. A doctor can approve a flagged claim if it looks clean. Flagging the member instead sends the claim to an audit committee, and the doctor can't close it until the committee clears it.

**Exercise 1: Review against Microsoft's Guidelines for Human-AI Interaction**

Microsoft has 18 guidelines. I picked the 9 that apply to the doctor's screen.

| **Guideline** | **What FWA did** | **Gap** | **Fix** |
| --- | --- | --- | --- |
| G1: Show what it can do | Risk level and reasons | No note on what FWA checks or misses | Short "what this checks" panel |
| G2: Show how well it works | Accuracy tracked internally from doctors' answers | Doctors weren't told how often each flag was wrong | Show how often other doctors marked that flag incorrect |
| G4: Show relevant information | Flags with threshold and breach, last 10 claims, price comparison | None, this worked well | Keep |
| G6: Reduce social bias | Thresholds by age group, gender and illness type; manual checks of flag rates by group | Fairness checks were manual | Automate the check |
| G9: Easy correction | Audit committee can clear a flagged member | None | Keep |
| G10: Hold back when unsure | Flags only fire when the threshold is crossed | A silent check can mean clean or not sure | Optional marker for low-confidence checks |
| G11: Explain why | Threshold and breach shown; document check highlighted the problem | Other checks didn't point to the exact line | Highlight the line or document used |
| G15: Detailed feedback | Each flag marked correct, incorrect or can't say | None, this worked well | Keep |
| G18: Tell users about changes | Current threshold shown on every claim | Changes not announced, but not needed since the live threshold is visible | None |
NIST also asks about people affected by an AI system who never see it. Here the design held up: members were told their profile was highlighted by automatic checks, suspicion was only raised after a person reviewed it, and the member was asked to answer a few questions before any action. The biggest real gap was G2. We knew how often each flag was wrong, but doctors didn't, so they had no reason to doubt a flag.

**Exercise 2: Redesign so a doctor can't rubber-stamp**

The weak spot is the "I have reviewed" checkbox, which can be ticked without reading anything. The per-flag answers were the strong part, so the redesign builds on them. It applies to High and Critical claims, where a wrong call does the most damage:

| **Step** | **Before** | **After** |
| --- | --- | --- |
| 1. Open the claim | Pop-up, then a checkbox | No checkbox. The flags themselves are what the doctor responds to. |
| 2. Answer each flag | Mark correct, incorrect or can't say | The answer options appear only after the doctor opens that flag's evidence (highlighted invoice line, matching claim, price comparison) |
| 3. How reliable is this flag | Tracked internally, not shown | For example: "Other doctors marked this flag incorrect on 12% of claims" |
| 4. Decide | Choose a decision | Only possible after every flag is answered. Rejecting for fraud, or approving a High or Critical claim, needs a short reason. |
Behind the screen, I would add three checks:

1. On a small random sample, the doctor gives their view before seeing the risk level, to test whether they judge for themselves.

2. Past claims with known outcomes are mixed into the queue now and then, to see if doctors catch them.

3. Each doctor's agreement rate and time per flagged claim are tracked. Agreeing every time in a few seconds triggers a quality review.

I would know it works if every flag gets answered, doctors overrule the AI at a steady rate rather than almost never, known cases get caught, and fewer rejected claims are paid later on appeal. It does add time per claim, but only for High and Critical, which were about 9 to 10% of claims.

**Reflection**

I built FWA mostly worried about fraud slipping through. Looking at it again, the people it can hurt are genuine members flagged by mistake, whose claims wait on an audit committee and whose money is delayed, and groups like younger members or frequent travellers flagged for who they are rather than what they did. Rejections went from 9 to 10% to about 14% after launch, and I can't say how much of that was real fraud and how much was mistakes. To find out, I would track appeals and rejected claims later paid from day one, and automate the group-by-group flag check I was doing by hand. Asking members to answer questions before acting was the right call, and I would keep it.

**AI use**

I used Claude (claude.ai) at set points in my process. The reading, the choice of examples, the exercises and the final decisions were mine:

1. I read all the articles.

2. I read the day's exercises to understand what I needed to show.

3. I picked the experience from my last company that best fit each exercise, explained the whole project to Claude and how it fits the exercise, and asked whether it was a good example. Based on Claude's response, I either changed the example or continued with it.

4. I did the exercise myself using the concepts from the readings, then gave it to Claude to polish, asking it to check with me before making any changes, since I own the result.

5. Once all the exercises were done, I asked Claude to polish each output so the reader can follow what I was thinking while doing the exercise.

6. I reviewed Claude's output before copying it into my document. For example, Claude suggested gaps in the FWA review screen against Microsoft's guidelines, which I checked against how the screen actually worked at Visit Health.

7. For the theory, I listed every topic I studied. Under each topic, I first copied in the content from the article, then added my own opinion and how I have used it in the past or plan to use it in future.

8. Once the theory part was done, I asked Claude to polish each section.

9. I reviewed Claude's output before copying it into my document.

10. I reviewed the whole document, made changes where needed, and then submitted it.


