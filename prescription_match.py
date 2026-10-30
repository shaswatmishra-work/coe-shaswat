"""Compare AI-extracted prescription fields against the values the doctor saved,
and report how many fields matched as a percentage."""


def normalize(value):
    """Turn a value into a form that's safe to compare.

    "Paracetamol 500 mg " and "paracetamol 500mg" should count as the same,
    so we lowercase and drop all whitespace. None becomes an empty string.
    """
    if value is None:
        return ""
    return "".join(str(value).lower().split())


def compare_fields(ai_fields, doctor_fields):
    """Check every field the doctor saved against what the AI extracted.

    The doctor's values are the source of truth, so we loop over those.
    A field the AI missed entirely is treated as None (a mismatch).
    """
    results = []
    for field, doctor_value in doctor_fields.items():
        ai_value = ai_fields.get(field)  # .get() returns None instead of crashing on a missing key
        results.append({
            "field": field,
            "ai": ai_value,
            "doctor": doctor_value,
            "matched": normalize(ai_value) == normalize(doctor_value),
        })
    return results


def match_percentage(results):
    if not results:
        return 0.0
    matched_count = sum(r["matched"] for r in results)  # True counts as 1, False as 0
    return matched_count / len(results) * 100


def print_report(results):
    print(f"{'Field':<14}{'AI value':<24}{'Doctor value':<24}Match")
    print("-" * 68)
    for r in results:
        mark = "yes" if r["matched"] else "NO"
        print(f"{r['field']:<14}{str(r['ai']):<24}{str(r['doctor']):<24}{mark}")
    print("-" * 68)
    print(f"Match: {match_percentage(results):.1f}%")


if __name__ == "__main__":
    ai_extracted = {
        "patient_name": "Ravi Kumar",
        "medicine": "Paracetamol 500 mg",
        "dosage": "1 tablet",
        "frequency": "Twice a day",
        "duration": "5 days",
        # "notes" is missing: the AI didn't extract it
    }

    doctor_saved = {
        "patient_name": "ravi kumar",
        "medicine": "Paracetamol 500mg",
        "dosage": "1 tablet",
        "frequency": "Thrice a day",
        "duration": "5 days",
        "notes": "After food",
    }

    print_report(compare_fields(ai_extracted, doctor_saved))
