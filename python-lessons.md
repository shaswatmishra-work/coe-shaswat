# Python Lessons: Prescription Match Project

**Goal:** Learn Python basics by building a script that compares AI-extracted prescription fields with the values a doctor saved, and calculates a match percentage.

**Finished script:** [prescription_match.py](prescription_match.py)

Run it:
```bash
python3 "/Users/shaswatmishra/COE Work/prescription_match.py"
```

Expected output:
```
patient_name  Ravi Kumar              ravi kumar              yes
medicine      Paracetamol 500 mg      Paracetamol 500mg       yes
dosage        1 tablet                1 tablet                yes
frequency     Twice a day             Thrice a day            NO
duration      5 days                  5 days                  yes
notes         None                    After food              NO
Match: 66.7%
```

## Roadmap

1. ✅ Variables, strings, `==`
2. ⬜ Functions with `def`: package the cleaning into `normalize()`
3. ⬜ Dictionaries: store a whole prescription as `{"medicine": ..., "dosage": ...}`
4. ⬜ `for` loops and `if`: go through every field
5. ⬜ Lists and counting: calculate the percentage
6. ⬜ Putting it together: rebuild the script yourself

---

## Lesson 1: Variables, strings, and comparing them

### Variables
A **variable** is a name for a value.
```python
ai_value = "Paracetamol 500 mg"
doctor_value = "paracetamol 500mg"
```
Text inside quotes is a **string**.

### Comparing with `==`
`==` asks "are these equal?" and gives back `True` or `False`.
```python
print(ai_value == doctor_value)   # False
```
Python compares strings **character by character**. `P` ≠ `p`, and `"500 mg"` ≠ `"500mg"`.

### String methods
Tools built into every string, called with a dot:

| Code | Result | What it does |
|---|---|---|
| `"Hello".lower()` | `"hello"` | lowercases everything |
| `"  hi  ".strip()` | `"hi"` | removes spaces at the start and end |
| `"a b  c".split()` | `["a", "b", "c"]` | breaks the text on **whitespace** into a list |
| `"".join(["a", "b", "c"])` | `"abc"` | glues a list back into one string |
| `"after-food".replace("-", " ")` | `"after food"` | swaps one piece of text for another |

### Chaining methods
Python runs a chain left to right:
```python
cleaned = "".join("Paracetamol 500 mg".lower().split())
print(cleaned)   # "paracetamol500mg"
```
Steps: lowercase it → split it on spaces → join the pieces with nothing in between.

### Exercise A (try it in the `python3` prompt)
1. `a = "Twice a day"` and `b = "twice  a day"` (two spaces)
2. Predict, then run: `a == b`
3. Clean both with `"".join(x.lower().split())` and compare again.

*Your result:* _(fill in)_

### Exercise B: Predict the match (done ✔ score 1/3)

| Pair | My answer | Correct | Why |
|---|---|---|---|
| `"5 Days"` vs `"5days"` | Match | ✅ Match | both become `"5days"` |
| `"1 tablet"` vs `"one tablet"` | Match | ❌ No match | `"1tablet"` vs `"onetablet"`: the digit `1` and the letters `one` are different characters |
| `"After food"` vs `"after-food"` | Match | ❌ No match | `.split()` only removes whitespace; the hyphen `-` stays |

### 💡 Key takeaway
**Python does exactly what you tell it, and nothing more.** It doesn't understand meaning. If `"1"` should equal `"one"`, or a hyphen should be ignored, you have to write code for it.
Real prescription data has this problem everywhere: "Twice a day", "BD" and "2x daily" all mean the same thing.

### Mini-challenge (open)
Change the cleaning so `"After food"` and `"after-food"` **do** match, using `.replace(...)`. Where in the chain does it go?

*My answer:* _(fill in)_

### Google this
- "python string methods"
- "python str.split vs str.strip"
- "python str.replace"
