# Discovery: Smart OCR v1 (Prescription Digitisation)

## Why

Doctors digitise printed prescriptions by typing the details in by hand. Smart OCR v1 removes most of that typing for the three most basic fields: **date, doctor name and patient name**. The doctor uploads a printed, single-page prescription. An AI reads it and fills in the three fields. The doctor checks each one against the document, corrects it if needed, and saves.

Every save keeps **both what the AI read and what the doctor finally saved**. That lets us find out whether the AI can be trusted, using real evidence instead of impressions, before we extend it to more fields or to real patient data.

This work is high risk because prescriptions contain patient health information (PHI), and HIPAA (US) applies. For that reason, v1 deliberately runs on **test or synthetic prescriptions only**. Real patient data stays blocked until the cloud AI provider has signed an agreement saying it will not train on or keep our data.

## Who

- **Doctors at one clinic** (several doctors). They are the only users of the screen. Each doctor has their own simple login, and every saved record shows which doctor saved it.
- **The clinic and product team** benefit from the saved data. It shows how accurate the AI is, how much time it saves, and how much it is actually used.
- **Patients** are affected indirectly. Their details must be read correctly and handled safely. The clinic's existing patient consent covers AI processing, so v1 does not need a consent step.

## Success Criteria

Success is measured three ways (the developer chose "all of the above"):

- **Accuracy:** at least **80% of fields are saved unedited** (the doctor keeps the AI's value) across the **first 50 or more prescriptions**.
  - **Golden test set:** before doctors rely on it, the AI is run on the 20 synthetic prescriptions in `Day 10 Project/smart-ocr-test-set/golden-set.csv`. Each AI value is compared with the expected date, doctor name and patient name using the per-field match score (see "What each saved record contains"). The same 80% target applies: at least 80% of the 60 fields (20 × 3) must be an exact match. This counts all 20 prescriptions, including the handwritten rx16–rx20, even though handwriting is out of scope on the screen (a deliberately stricter bar). The golden set is re-run whenever the AI provider or its instructions change.
- **Time saved:** the time from upload to save is recorded for every prescription. It is clearly shorter than a one-off baseline of typing a prescription in by hand.
- **Adoption:** doctors digitise a large share of prescriptions through this screen rather than typing them in by hand. This is measured as the share of prescriptions digitised through the screen.
- **Safety:** no real patient data goes to the AI provider in v1, and no uploaded prescription file is kept after the doctor saves.

**Later-phase outcome measures** (beyond v1; they need real claims, so they start once real patient data is allowed). Reference points come from the copilot at Visit Health:

| Outcome | Visit Health before the copilot | Visit Health after |
|---|---|---|
| Doctor time per claim | 30 minutes | about 8 minutes |
| Share of claims the insurer sends back for wrong digitisation | 8% | 2% |

<!-- -------- bee-comment -------- -->
> **@developer**: Add two later-phase outcome measures: doctor time per claim (30 minutes before the copilot at Visit Health, about 8 after) and the share of claims the insurer sends back for wrong digitisation (8% before, 2% after).
> **@bee**: Added a "Later-phase outcome measures" table with both measures and the Visit Health before/after figures as reference points. Marked them as starting once real patient data is allowed, since v1 runs on test data and has no real claims. Added open question 15 on where claim time and insurer send-backs will be measured, since nothing in v1 captures them yet.
> - [ ] mark as resolved
<!-- -------- /bee-comment -------- -->

<!-- -------- bee-comment -------- -->
> **@developer**: Use smart-ocr-test-set/golden-set.csv (20 synthetic prescriptions with expected values) as the golden test set for the accuracy target.
> **@bee**: Added a "Golden test set" point under Accuracy. The AI is run on the 20 prescriptions and each value is scored against the expected values, with the same 80% target (of 60 fields). The file is at `Day 10 Project/smart-ocr-test-set/golden-set.csv` inside COE Work, so that's the path used. The 50+ prescription measure on doctors' saved records stays as a second check in real use.
> - [ ] mark as resolved
<!-- -------- /bee-comment -------- -->

## Problem Statement

Typing prescription details in by hand is slow and repetitive work for doctors. An AI could do most of it, but nobody yet knows how often it reads the date, doctor name and patient name correctly. Smart OCR v1 pre-fills those three fields, lets the doctor confirm or correct each one, and records the AI's answer next to the doctor's. That pairing measures accuracy, time saved and adoption. It does this safely, on test data, before any real patient data is involved.

## Hypotheses

- **H1:** A cloud vision AI can read the date, doctor name and patient name from a printed, single-page prescription well enough that at least 80% of fields are saved unedited. *(Confirmed or rejected by the accuracy measure. A rejection means rethinking the provider before adding fields or real data.)*
- **H2:** Pre-filling makes digitising a prescription faster than typing it by hand, even after the time doctors spend checking and correcting. *(Confirmed or rejected by comparing upload-to-save times with the manual baseline.)*
- **H3:** Doctors trust the pre-fill enough to use the screen for most prescriptions. *(Confirmed or rejected by the adoption share.)*
- **H4 (riskiest assumption):** Showing where each value was read, as a box on the prescription image, lets the doctor check a field without re-reading the whole page. *(Evidence: at Visit Health, doctors kept re-reading the whole prescription until a box showed where each value was read. If this fails, doctors re-read every page, the time saving in H2 disappears, and H3's adoption follows it down. It also depends on the AI provider returning reliable positions, which is not yet proven.)*

<!-- -------- bee-comment -------- -->
> **@developer**: Replace H4. At Visit Health, doctors kept re-reading the whole prescription until we showed a box on the image where each value was read. New H4: showing where each value was read lets the doctor check a field without re-reading the page. Make this the riskiest assumption.
> **@bee**: Replaced H4 with the "where it was read" box hypothesis, labelled it the riskiest assumption, and recorded the Visit Health evidence. Explained why it's riskiest: H2 and H3 depend on it, and it needs the AI to return accurate positions. The old H4 (revert is enough review support) is gone; revert stays in Phase 2 as a feature. Added "Riskiest assumption" under the list so it stands out.
> - [ ] mark as resolved
<!-- -------- /bee-comment -------- -->
- **H5:** Keeping only the field values and deleting the uploaded file still gives us everything we need to measure accuracy. *(We scope OUT keeping files. If accuracy questions can't be answered without the image, we revisit this. The "where it was read" box only needs the image while the doctor is checking, which the browser's own copy covers.)*

**Riskiest assumption: H4.** Test it first, in Phase 1.

## Decisions Made in Discovery

| Topic | Decision |
|---|---|
| AI reading | Cloud vision AI. v1 runs on test or synthetic prescriptions only. Real patient data is blocked until a data agreement is signed (no training on our data, no retention). |
| Regulation | HIPAA (US) |
| Uploaded file | Deleted once the record is saved. Only the field values are kept. |
| Consent | Covered by the clinic's existing patient consent. No consent flow in v1. |
| Users | One clinic, several doctors, each with a simple login. Every record shows who saved it. |
| Low confidence | Always pre-fill whatever the AI read. No confidence handling in v1. |
| Files accepted | JPG, PNG and PDF, up to 10 MB. A PDF with more than one page is rejected with the message "Please upload a single-page prescription". |
| Screens under 1024px | Show the message "This screen is designed for desktop or laptop. Please widen your window." |
| While the AI is reading | Skeleton placeholders in the three fields with the text "Reading prescription…", announced to screen readers |
| Preview controls | Zoom in and zoom out only. No rotate or pan. |
| Visual design | As set out in `.claude/DESIGN.md`: Clinical & Calm, Sanzo Wada palette 259, IBM Plex, AI-filled / Edited / Not detected indicators, "AI read: … / Revert to AI value" on edited fields |

### What each saved record contains

```
DigitisedPrescription:
  savedBy            (the doctor who saved it)
  savedAt            (date and time)
  uploadedAt         (start of the upload-to-save timing)
  fileName, fileType (the file itself is not kept)
  fields: date, doctorName, patientName — each with:
    aiValue          (what the AI read; empty if it read nothing)
    finalValue       (what the doctor saved)
    status           accepted as read | edited | edited then reverted
    matchScore       (AI value compared with the final value)
      exactMatch     yes | no — after tidying both values: trim, collapse repeated spaces, ignore capitals
      similarity     0–100% — how close the two tidied values are
```

The same match score compares the AI value with the expected value when the golden test set is run. Similarity is character-level (the share of characters that don't need changing). Dates are compared as calendar dates, so a correct date printed in another format (for example "10 Nov 2025" vs 10/11/2025) is an exact match. The position of each value is used on screen only and is not stored on the record.

<!-- -------- bee-comment -------- -->
> **@developer**: Also store a match score per field: exact match after tidying spaces and capitals, plus a similarity percentage.
> **@bee**: Added `matchScore` to each field with `exactMatch` (after trimming, collapsing repeated spaces and ignoring capitals) and `similarity` (0–100%), comparing the AI value with the doctor's final value. Reused the same score for the golden test set. Added open questions 12 and 13: how dates are compared (the AI's raw text vs the normalised DD/MM/YYYY), and which similarity method to use.
> - [ ] mark as resolved
<!-- -------- /bee-comment -------- -->

## Out of Scope

- Real patient prescriptions. They stay blocked until the provider's data agreement is signed.
- Fields beyond date, doctor name and patient name (for example, medicines and dosages).
- Handwritten prescriptions, and prescriptions longer than one page.
- Confidence scores, highlighting doubtful values, or any "low confidence" behaviour. (The "where it was read" box is in scope: it shows location, not confidence.)
- Running the AI locally, or comparing more than one AI provider.
- Keeping uploaded prescription files after save.
- A consent capture step.
- Layouts for mobile or tablet. Below 1024px only a message is shown.
- Rotating or panning the preview.
- Dark mode.
- Several clinics, or different user roles beyond "doctor".
- Capturing the image with a camera. Upload from the device only.

## Milestone Map

### Phase 1: Walking skeleton. Upload, pre-fill, see where it was read, correct, save
The thinnest end-to-end path. A doctor gets from a prescription to a saved record with both values, and can check each field against the spot on the image where it was read (tests H4, the riskiest assumption).
- The doctor logs in with their own account.
- The doctor uploads a JPG or PNG prescription (test data) and sees it in the preview panel.
- The cloud AI reads the date, doctor name and patient name, and the three fields are pre-filled.
- The AI also returns the position of each value on the image. When the doctor focuses a field, that area is highlighted with a box on the preview. A field the AI didn't read has no box.
- The doctor edits any field and saves.
- The saved record holds the AI value and the final value for each field, plus who saved it, when, and the file name and type.
- The uploaded file is deleted once the record is saved.

<!-- -------- bee-comment -------- -->
> **@developer**: Move the "where it was read" box into Phase 1: the AI returns the position of each value, and focusing a field highlights that area on the preview.
> **@bee**: Added it to Phase 1: the AI returns each value's position, and focusing a field draws a box around that area on the preview (no box when the AI read nothing). Renamed the phase and tied it to H4. Also updated the `reading/` module to return positions, and removed "highlighting" from Out of Scope (doubtful-value highlighting stays out). Added open question 14: the AI provider must return reliable positions, which narrows the provider choice. This changes the approved Phase 1 spec and the design brief, which both need updating.
> - [ ] mark as resolved
<!-- -------- /bee-comment -------- -->

### Phase 2: The complete review experience
Builds on Phase 1 so that checking and correcting is quick and trustworthy.
- Each field shows its state (AI-filled, Edited, Not detected) with an icon, a text tag and a background.
- Edited fields show "AI read: …" and a "Revert to AI value" action. Each field's status (accepted as read / edited / edited then reverted) is saved.
- Skeleton fields with "Reading prescription…" appear while the AI reads, announced to screen readers.
- The preview has zoom in and zoom out.
- PDF uploads are accepted. Multi-page PDFs and files over 10 MB, or of other types, are rejected with clear messages.
- Screens under 1024px show the "designed for desktop or laptop" message.
- Clear error messages appear when the upload or the AI reading fails.

### Phase 3: Measuring success
Turns the saved records into answers for H1 to H3.
- Upload-to-save duration is recorded for every record.
- An accuracy view shows the share of fields saved unedited, per field and overall, against the 80% / 50+ prescription target.
- A time comparison shows average upload-to-save duration against the manual typing baseline.
- An adoption view shows the share of prescriptions digitised through this screen.

## Module Structure
*(Greenfield. Named by what each part owns, not by technology.)*

- `accounts/`: owns Doctor and Login. Depends on (none).
- `documents/`: owns the uploaded prescription, the file rules (type, size, single page) and deleting the file after save. Depends on (none).
- `reading/`: owns sending a document to the cloud AI and returning the three values it read, with the position of each on the image. It is kept separate so the provider can be changed or reviewed without touching the rest. Depends on `documents/`.
- `digitisation/`: owns DigitisedPrescription, field values (AI value, final value) and field status. Depends on `accounts/`, `documents/`, `reading/`.
- `insights/`: owns the accuracy, time and adoption measures. Depends on `digitisation/`.
- `screen/`: owns the doctor-facing digitisation screen (preview, fields, provenance, revert, save). Depends on `accounts/`, `digitisation/`.

## Open Questions

1. **Which cloud AI provider?** Under HIPAA, the agreement it signs is usually a Business Associate Agreement (BAA). Will the chosen provider sign one that also guarantees no training and no retention?
2. **How is "test data only" enforced in v1?** Is it a process rule, or a visible gate in the product? Who supplies the test or synthetic prescriptions, and how many are needed to reach 50+?
3. **How are doctor accounts created and managed?** This covers who sets them up, forgotten passwords, and removing a doctor who leaves.
4. **How long are saved records kept?** We decided to delete the file, but not how long the field values (which include patient names) are retained.
5. **Can saved records be viewed, corrected or deleted later?** Nothing was decided about anything after save.
6. **What happens when the AI service fails or is slow?** Can the doctor fall back to typing the fields by hand? Is there a time limit?
7. **What is the adoption baseline?** Where does the total number of prescriptions come from, so we can work out the share digitised through this screen?
8. **Who records the manual typing baseline, when, and on how many prescriptions?**
9. **How do "Not detected" fields count for accuracy?** For example, if the AI read nothing and the doctor typed a value, is that a miss? And what status does a field get if the doctor edits again after reverting?
10. **Which date format does the date field use?** Should the saved value be normalised to one format?
11. **Beyond who saved each record, does HIPAA need a log of who viewed records?** This depends on whether records can be viewed after save (question 5).
12. ~~How is the date compared for the match score?~~ **Decided (2 Nov 2026):** as calendar dates.
13. ~~Which similarity method gives the percentage?~~ **Decided (2 Nov 2026):** character-level, the same for saved records and the golden set.
14. **Can the chosen AI provider return reliable positions for each value?** Not every cloud vision AI returns accurate boxes. This narrows the provider choice in question 1 and should be checked on the golden set early. *(Decided 2 Nov 2026: positions are used on screen only, not stored on the record. Still open: how position reliability is checked, since the golden set has no expected positions.)*
15. **Where will doctor time per claim and insurer send-backs be measured?** v1 captures neither. Needs a source (claims system or insurer reports) before the later-phase outcome measures can be tracked.

## Revised Assessment
Size: EPIC. Triage said FEATURE, but per-doctor logins, a cloud AI integration under HIPAA constraints, and success measurement add up to three separate phases that each deliver value.
Risk: HIGH. This is patient health information under HIPAA. It is reduced in v1 by using test data only and deleting files after save.
Greenfield: yes

[x] Reviewed
