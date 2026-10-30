# Spec: Smart OCR v1 — Phase 1 (Walking Skeleton)

## Overview
A signed-in doctor uploads a printed, single-page JPG or PNG prescription (test data only). A cloud AI reads it and pre-fills date, doctor name and patient name. The doctor edits any field and saves. Every saved record keeps the AI's value and the doctor's final value for each field, so later phases can measure accuracy, time saved and adoption.

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

## Slice 4: Doctor edits, saves, and the screen resets
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

## Indicative Shapes

```
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

Doctor: { id, name, email, password (hashed) }
```

## Out of Scope
- Field provenance indicators (AI-filled / Edited / Not detected tags, icons and tints)
- "AI read: …" line and "Revert to AI value" action, and the "edited then reverted" status
- Skeleton "Reading prescription…" loading state
- Zoom in / zoom out on the preview
- PDF uploads, the 10 MB limit and its message, and the multi-page rejection message
- The "designed for desktop or laptop" message under 1024px
- Polished error messages for upload and AI failures (Phase 1 shows plain errors)
- Accuracy, time-comparison and adoption views (Phase 3)
- Retention period for saved records (PRD open question 4)
- Choosing the AI provider and signing the BAA (PRD open question 1)
- Adoption baseline and manual typing baseline (PRD open questions 7, 8)
- Viewing, correcting or deleting saved records in the app, and the view/access log
- Self-signup, password reset, account deactivation screens, and login lockout
- Technical blocking of real patient data (enforced by the banner and a written process rule only)
- Real patient prescriptions, handwritten or multi-page prescriptions, fields beyond the three, confidence handling, camera capture, multiple clinics or roles, dark mode

## Assumptions (developer can change during review)
1. **Basic rejection of non-JPG/PNG files in Phase 1.** This keeps the skeleton from breaking. The wording is a placeholder; Phase 2 adds the full PDF, size and multi-page rules.
2. **AI time limit is 30 seconds.** The developer said "e.g. 30s".
3. **Unparseable AI dates are pre-filled as raw text.** This follows "always pre-fill whatever the AI read". The doctor must correct it before save passes date validation.
4. **Status compares the final value with the pre-filled value.** A date the AI read as a valid calendar date and the doctor left unchanged counts as "accepted as read", even though the stored form is normalised.
5. **Empty fields can be saved.** No field is mandatory in Phase 1. Only an entered date must be a valid DD/MM/YYYY date.
6. **The doctor signs in with their email**, as implied by the "Email or password is incorrect" message.

## Technical Context
- Greenfield. The stack, framework and test tooling are left to architecture.
- Module boundaries (from discovery): `accounts/` (Doctor, login, sessions), `documents/` (upload, file type rule, deletion), `reading/` (cloud AI call, behind its own boundary so the provider can change), `digitisation/` (DigitisedPrescription, field values, status), `screen/` (doctor-facing UI).
- Design: follow `.claude/DESIGN.md` for palette 259 tokens, IBM Plex, the two-column layout (preview about 7/12, fields about 5/12), the field order Date then Doctor name then Patient name then Save, one primary Save button, 44x44px targets, visible focus, labelled inputs, errors linked via `aria-describedby`, and status messages announced in a polite live region.
- Developer decisions for Phase 1: setup-script accounts; manual entry fallback after a failure or 30s timeout; dates shown as DD/MM/YYYY and validated, with the AI raw text kept; always-visible test-data banner; confirm and reset after save with no post-save access; file deleted right after the AI read; `uploadedAt` and accepted/edited status captured now; 15-minute inactivity sign-out with a generic login error.
- Risk level: HIGH (HIPAA, PHI). Reduced by test data only, deleting the file right after the AI read, and no in-app access to saved records.

[x] Reviewed
