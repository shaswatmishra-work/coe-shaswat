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
- **Time saved:** the time from upload to save is recorded for every prescription. It is clearly shorter than a one-off baseline of typing a prescription in by hand.
- **Adoption:** doctors digitise a large share of prescriptions through this screen rather than typing them in by hand. This is measured as the share of prescriptions digitised through the screen.
- **Safety:** no real patient data goes to the AI provider in v1, and no uploaded prescription file is kept after the doctor saves.

## Problem Statement

Typing prescription details in by hand is slow and repetitive work for doctors. An AI could do most of it, but nobody yet knows how often it reads the date, doctor name and patient name correctly. Smart OCR v1 pre-fills those three fields, lets the doctor confirm or correct each one, and records the AI's answer next to the doctor's. That pairing measures accuracy, time saved and adoption. It does this safely, on test data, before any real patient data is involved.

## Hypotheses

- **H1:** A cloud vision AI can read the date, doctor name and patient name from a printed, single-page prescription well enough that at least 80% of fields are saved unedited. *(Confirmed or rejected by the accuracy measure. A rejection means rethinking the provider before adding fields or real data.)*
- **H2:** Pre-filling makes digitising a prescription faster than typing it by hand, even after the time doctors spend checking and correcting. *(Confirmed or rejected by comparing upload-to-save times with the manual baseline.)*
- **H3:** Doctors trust the pre-fill enough to use the screen for most prescriptions. *(Confirmed or rejected by the adoption share.)*
- **H4:** Showing the AI's original value with a "Revert to AI value" action on edited fields is enough review support. No confidence scores or highlighting are needed in v1. *(The "edited then reverted" status gives an early signal.)*
- **H5:** Keeping only the field values and deleting the uploaded file still gives us everything we need to measure accuracy. *(We scope OUT keeping files. If accuracy questions can't be answered without the image, we revisit this.)*

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
```

## Out of Scope

- Real patient prescriptions. They stay blocked until the provider's data agreement is signed.
- Fields beyond date, doctor name and patient name (for example, medicines and dosages).
- Handwritten prescriptions, and prescriptions longer than one page.
- Confidence scores, highlighting doubtful values, or any "low confidence" behaviour.
- Running the AI locally, or comparing more than one AI provider.
- Keeping uploaded prescription files after save.
- A consent capture step.
- Layouts for mobile or tablet. Below 1024px only a message is shown.
- Rotating or panning the preview.
- Dark mode.
- Several clinics, or different user roles beyond "doctor".
- Capturing the image with a camera. Upload from the device only.

## Milestone Map

### Phase 1: Walking skeleton. Upload, pre-fill, correct, save
The thinnest end-to-end path. A doctor gets from a prescription to a saved record with both values.
- The doctor logs in with their own account.
- The doctor uploads a JPG or PNG prescription (test data) and sees it in the preview panel.
- The cloud AI reads the date, doctor name and patient name, and the three fields are pre-filled.
- The doctor edits any field and saves.
- The saved record holds the AI value and the final value for each field, plus who saved it, when, and the file name and type.
- The uploaded file is deleted once the record is saved.

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
- `reading/`: owns sending a document to the cloud AI and returning the three values it read. It is kept separate so the provider can be changed or reviewed without touching the rest. Depends on `documents/`.
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

## Revised Assessment
Size: EPIC. Triage said FEATURE, but per-doctor logins, a cloud AI integration under HIPAA constraints, and success measurement add up to three separate phases that each deliver value.
Risk: HIGH. This is patient health information under HIPAA. It is reduced in v1 by using test data only and deleting files after save.
Greenfield: yes

[x] Reviewed
