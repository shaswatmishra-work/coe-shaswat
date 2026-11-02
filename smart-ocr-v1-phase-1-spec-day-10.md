# Spec: Smart OCR v1 — Phase 1 (Walking Skeleton)

## Overview
A signed-in doctor uploads a printed, single-page JPG or PNG prescription (test data only). A cloud AI reads it and pre-fills date, doctor name and patient name. It also returns where on the image it read each value. When the doctor focuses a field, a box on the preview shows that spot. The doctor edits any field and saves. Every saved record keeps the AI's value, the doctor's final value and a match score for each field, so later phases can measure accuracy, time saved and adoption. A repeatable golden-set check measures the AI on 20 synthetic prescriptions against the 80% target.

Phase 1 tests H4, the riskiest assumption: showing where each value was read lets the doctor check a field without re-reading the whole page. If it fails, the time saving (H2) and adoption (H3) fail with it.

Source: `docs/specs/smart-ocr-v1-discovery.md` (Phase 1), `.claude/DESIGN.md`. Developer decisions for Phase 1 are listed under Technical Context.

## Slice 1: Doctor signs in
- [ ] An admin command creates a doctor account with a name, email and starting password
- [ ] A doctor can sign in with their email and password
- [ ] Shows "Email or password is incorrect" when the email is unknown
- [ ] Shows "Email or password is incorrect" when the password is wrong
- [ ] Visiting the digitisation screen while signed out redirects to the sign-in page
- [ ] The digitisation screen always shows the banner "Test data only. Do not upload real patient prescriptions"
- [ ] A doctor can sign out from the digitisation screen
- [ ] The doctor is signed out automatically after 15 minutes of inactivity
- [ ] Automatic sign-out clears any unsaved upload, preview and field values from the screen

## Slice 2: Doctor uploads a prescription and sees it in the preview
- [ ] Before upload, the preview panel shows an upload drop zone that can be operated by keyboard
- [ ] A doctor can upload a JPG prescription from their device
- [ ] A doctor can upload a PNG prescription from their device
- [ ] The uploaded image appears in the preview panel, fit to width
- [ ] The preview has the text alternative "Uploaded prescription: <file name>"
- [ ] Shows "Please upload a JPG or PNG prescription" when the file is any other type, and nothing is sent to the AI *(assumption, see below)*
- [ ] Upload is rejected for a doctor who is not signed in

## Slice 3: AI pre-fills date, doctor name and patient name
- [ ] After upload, the Date, Doctor name and Patient name fields are pre-filled with what the AI read
- [ ] A field the AI could not read is left empty and editable
- [ ] A date the AI read that is a valid calendar date is shown as DD/MM/YYYY
- [ ] A date the AI read that is not a valid calendar date is pre-filled as the AI's raw text
- [ ] When the AI has not answered within 30 seconds, shows a plain error and all three fields are empty and editable
- [ ] When the AI reading fails, shows a plain error and all three fields are empty and editable
- [ ] The uploaded file is deleted from the server as soon as the AI returns its values
- [ ] The uploaded file is deleted from the server as soon as the AI reading fails or times out
- [ ] The preview stays visible after the server copy is deleted (it is shown from the browser's own copy)

## Slice 4: Doctor sees where each value was read (tests H4)
- [ ] When the doctor focuses a field the AI read, a box on the preview surrounds the area of the image where that value was read, highlighted as described in DESIGN.md
- [ ] The box appears whether the field is focused by keyboard or by mouse
- [ ] When focus moves to another field, the box moves to the area where that field's value was read
- [ ] When focus leaves all three fields (for example to Save or the upload control), the box is removed
- [ ] After the doctor edits a field, focusing it still shows the box where the AI read the original value
- [ ] Focusing a field the AI could not read shows no box
- [ ] Focusing a field for which the AI returned a value but no position shows no box *(assumption, see below)*
- [ ] No box is shown for any field when the AI reading failed or timed out
- [ ] The box surrounds the same area of the image at the preview's displayed size (fit to width), not at the image's original size
- [ ] The box still appears over the same area after the server copy of the file is deleted (it is drawn on the browser's own copy)
- [ ] The AI reading returns, with each value it read, that value's position on the image
- [ ] Positions are used on screen only: the saved record holds no positions

## Slice 5: Doctor edits, saves, and the screen resets
- [ ] The doctor can edit any of the three fields before saving
- [ ] Shows an error on the Date field and does not save when the date is not a valid DD/MM/YYYY calendar date
- [ ] Saving shows "Prescription saved"
- [ ] After saving, the screen resets to the empty upload state
- [ ] The saved record holds the AI value and the final value for each of date, doctor name and patient name
- [ ] The saved record holds an empty AI value for every field when the AI failed or timed out
- [ ] The saved record holds who saved it, when it was saved, when the file was uploaded, and the file name and type
- [ ] Each field is saved with status "accepted as read" when its final value equals its pre-filled AI value, and "edited" otherwise
- [ ] The saved date's final value is stored in one normalised calendar-date form, independent of display format
- [ ] Shows an error, keeps the doctor's entered values on screen and saves nothing when the save fails
- [ ] For doctor name and patient name, the saved record holds exactMatch "yes" when the AI value and final value are equal after trimming, collapsing repeated spaces and ignoring capitals, and "no" otherwise (e.g. " rahul  MEHTA" and "Rahul Mehta" match)
- [ ] For each field, the saved record holds a character-level similarity from 0 to 100% between the tidied AI value and the tidied final value: the share of characters that don't need changing to turn one into the other (e.g. "Rahul Mehta" and "Rahul Mehra" score about 91%)
- [ ] Similarity is 100% when the tidied AI value and tidied final value are identical
- [ ] A field whose AI value is empty and whose final value is not empty is saved with exactMatch "no" and similarity 0%
- [ ] For the date field, exactMatch is "yes" when the AI's date and the final date are the same calendar date, whatever format the AI read it in (e.g. AI "10 Nov 2025" and final 10/11/2025 match)
- [ ] For the date field, exactMatch is "no" when the AI's raw text cannot be read as a calendar date
- [ ] For the date field, similarity compares both dates written as DD/MM/YYYY when the AI's text can be read as a date, and the AI's raw text with the DD/MM/YYYY final value when it cannot *(assumption, see below)*

## Slice 6: Golden-set accuracy check
- [ ] A developer can run one command that sends each of the 20 golden-set prescriptions to the AI reader and prints a report
- [ ] The report lists, for each prescription and field, the AI value, the expected value, exactMatch and similarity
- [ ] The report shows the exact-match rate for each of date, doctor name and patient name, out of 20
- [ ] The report shows the overall exact-match rate across all 60 fields
- [ ] The report states whether the overall exact-match rate meets the 80% target, counting all 20 prescriptions, including the handwritten rx16–rx20
- [ ] The check scores each field with the same match score as saved records (Slice 5)
- [ ] A field with an empty expected value (for example rx07's date) is an exact match only when the AI also read nothing
- [ ] A prescription the AI fails on or times out on is scored with empty AI values and the run continues with the next prescription *(assumption, see below)*
- [ ] Shows an error naming the missing file and reports nothing when the golden-set CSV or one of its images is missing
- [ ] The check sends only the 20 synthetic golden-set images to the AI and saves no prescription records *(assumption, see below)*

## Indicative Shapes

```
AI reading result (reading/ → screen):
  date | doctorName | patientName:
    value        string, empty if not read (date: AI raw text)
    position     area on the image where the value was read; absent if not read or not returned

DigitisedPrescription:
  savedBy        doctor id
  savedAt        timestamp
  uploadedAt     timestamp (upload start)
  fileName, fileType   (file itself not kept)
  fields:
    date | doctorName | patientName:
      aiValue      string, empty if not read / AI failed (date: AI raw text)
      finalValue   string (date: normalised calendar date)
      status       "accepted as read" | "edited"
      matchScore:
        exactMatch   yes | no   (after trim, collapse repeated spaces, ignore capitals)
        similarity   0–100%, character-level
      (positions are not stored: screen only)

Golden-set report:
  rows:    file, field, aiValue, expectedValue, exactMatch, similarity
  perField exact-match rate: date, doctorName, patientName (of 20)
  overall  exact-match rate (of 60), meets 80% target: yes | no

Doctor: { id, name, email, password (hashed) }
```

## Out of Scope
- Field provenance indicators (AI-filled / Edited / Not detected tags, icons and tints)
- "AI read: …" line and "Revert to AI value" action, and the "edited then reverted" status
- Skeleton "Reading prescription…" loading state
- Zoom in / zoom out on the preview. When zoom arrives in Phase 2, the "where it was read" box must follow the zoom and stay over the same area of the image
- Confidence scores or highlighting doubtful values. The box shows location only, not confidence
- Scoring how accurate the AI's positions are in the golden-set check (the golden set has no expected positions, and positions are not stored on records)
- PDF uploads, the 10 MB limit and its message, and the multi-page rejection message
- The "designed for desktop or laptop" message under 1024px
- Polished error messages for upload and AI failures (Phase 1 shows plain errors)
- Accuracy, time-comparison and adoption views, including an accuracy dashboard over saved records or golden-set runs (Phase 3)
- Doctor time per claim and insurer send-back measures (later phase, PRD open question 15)
- Retention period for saved records (PRD open question 4)
- Choosing the AI provider and signing the BAA (PRD open question 1)
- Adoption baseline and manual typing baseline (PRD open questions 7, 8)
- Viewing, correcting or deleting saved records in the app, and the view/access log
- Self-signup, password reset, account deactivation screens, and login lockout
- Technical blocking of real patient data (enforced by the banner and a written process rule only)
- Real patient prescriptions, handwritten or multi-page prescriptions on the screen, fields beyond the three, camera capture, multiple clinics or roles, dark mode

## Assumptions (developer can change during review)
1. **Basic rejection of non-JPG/PNG files in Phase 1.** This keeps the skeleton from breaking. The wording is a placeholder; Phase 2 adds the full PDF, size and multi-page rules.
2. **AI time limit is 30 seconds.** The developer said "e.g. 30s".
3. **Unparseable AI dates are pre-filled as raw text.** This follows "always pre-fill whatever the AI read". The doctor must correct it before save passes date validation.
4. **Status compares the final value with the pre-filled value.** A date the AI read as a valid calendar date and the doctor left unchanged counts as "accepted as read", even though the stored form is normalised.
5. **Empty fields can be saved.** No field is mandatory in Phase 1. Only an entered date must be a valid DD/MM/YYYY date.
6. **The doctor signs in with their email**, as implied by the "Email or password is incorrect" message.
7. **A value returned without a position gets no box.** The field is still pre-filled with the value; only the box is missing. The PRD only says a field the AI didn't read has no box.
8. **A golden-set prescription the AI fails on is scored with empty AI values**, the same as the screen treats a failure (Slice 3). It counts as a miss unless the expected value is also empty.
9. **Golden-set runs do not create saved records.** This keeps the 50+ prescription accuracy measure on doctors' saved records separate from the golden-set check.
10. **Date similarity** compares both dates written as DD/MM/YYYY when the AI's text can be read as a date, and the raw text otherwise. The developer chose to compare dates as dates for exactMatch; this extends the same idea to similarity.

## Decisions on this phase's open questions (developer, 2 Nov 2026)
1. **Date match score:** compare as calendar dates, so a correct date printed in a different format (e.g. "10 Nov 2025") is an exact match. Slice 5.
2. **Similarity method:** character-level (share of characters that don't need changing). Same method for saved records and the golden set. Slices 5 and 6.
3. **Positions:** used on screen only, not stored on the saved record. Slice 4. Still open at PRD level: how the provider's position reliability is checked (PRD open question 14).
4. **Focus leaves the fields:** the box is removed. Slice 4.
5. **Edited fields:** keep showing the box where the AI read the original value. Slice 4.
6. **Handwritten golden-set prescriptions:** the 80% target counts all 20 prescriptions (60 fields), including handwritten rx16–rx20, even though handwriting is out of scope on the screen. This is a stricter bar. Slice 6.

## Technical Context
- Greenfield. The stack, framework and test tooling are left to architecture.
- Module boundaries (from discovery): `accounts/` (Doctor, login, sessions), `documents/` (upload, file type rule, deletion), `reading/` (cloud AI call returning each value and its position on the image, behind its own boundary so the provider can change), `digitisation/` (DigitisedPrescription, field values, status, match score), `screen/` (doctor-facing UI, including the "where it was read" box).
- The match score rule (tidying, exactMatch, similarity) has one definition, used by both saved records (Slice 5) and the golden-set check (Slice 6).
- Golden set: `Day 10 Project/smart-ocr-test-set/golden-set.csv` (columns `file, expected_date, expected_doctor_name, expected_patient_name, what_it_tests`; 20 synthetic prescriptions, rx01.jpg to rx20.jpg alongside). Expected dates are DD/MM/YYYY; rx07 has no expected date. Re-run whenever the AI provider or its instructions change.
- Design: follow `.claude/DESIGN.md` for palette 259 tokens, IBM Plex, the two-column layout (preview about 7/12, fields about 5/12), the field order Date then Doctor name then Patient name then Save, one primary Save button, 44x44px targets, visible focus, labelled inputs, errors linked via `aria-describedby`, status messages announced in a polite live region, and the look of the "where it was read" box.
- Developer decisions for Phase 1: setup-script accounts; manual entry fallback after a failure or 30s timeout; dates shown as DD/MM/YYYY and validated, with the AI raw text kept; always-visible test-data banner; confirm and reset after save with no post-save access; file deleted right after the AI read; `uploadedAt` and accepted/edited status captured now; 15-minute inactivity sign-out with a generic login error; "where it was read" box on focus (H4); per-field match score on the saved record; golden-set check against the 80% target.
- Riskiest assumption: H4. Slice 4 depends on the AI provider returning usable positions (PRD open question 14), which also narrows the provider choice.
- Risk level: HIGH (HIPAA, PHI). Reduced by test data only, deleting the file right after the AI read, no in-app access to saved records, and a golden set made only of synthetic prescriptions.

[x] Reviewed
