# AI Interview Practice Bot (Multiple-Choice Edition)

A capstone project that simulates interview practice with a fixed set of
multiple-choice questions, instant feedback with explanations, and a
structured end-of-session summary. One shared `core/` engine powers two
interfaces: a Tkinter desktop app and a Flask web app.

## Features

- 19 fixed questions across four categories: **Technical**, **Aptitude**,
  **Communication**, **Personal / Background** (easy / medium / hard)
- Four options per question, shuffled each session
- Instant feedback: correct/incorrect, the right answer, and an explanation
- Session summary: overall score, per-category breakdown, strengths,
  areas to improve, and a review of every mistake
- Deterministic scoring (an answer is simply right or wrong)

## Project structure

```
core/
  questions.py   # fixed question bank (options, answer index, explanation)
  scoring.py     # evaluates one selected option
  session.py     # session flow, option shuffling, summary
desktop_app.py   # Tkinter UI
web_app.py       # Flask UI
templates/ static/
tests/test_core.py
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python desktop_app.py          # desktop
python web_app.py              # web -> http://127.0.0.1:5000
python -m pytest               # tests
```

Optional env vars for the web app: `SECRET_KEY` (stable session cookies),
`FLASK_DEBUG=1` (debug mode).

## Adding questions

Append a dict to `QUESTION_BANK` in `core/questions.py`:

```python
{"id": "tech_07", "category": "technical", "difficulty": "easy",
 "text": "Your question?",
 "options": ["A", "B", "C", "D"],
 "answer": 2,                      # index of the correct option
 "explanation": "Why C is right."}
```

`tests/test_core.py` checks the bank for duplicate ids, bad answer
indexes, and duplicate options.

## Scoring

Score = correct answers / total questions in the session. Skipped
questions count as 0. The first answer submitted for a question is final.

## Roadmap

- Timed mode and per-question timers
- Save results to track progress across sessions
- Role-specific question sets
