import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from core.questions import QUESTION_BANK, get_categories, get_questions
from core.scoring import evaluate_answer
from core.session import InterviewSession


def test_bank_is_well_formed():
    ids = [q["id"] for q in QUESTION_BANK]
    assert len(ids) == len(set(ids)), "duplicate question ids"
    for q in QUESTION_BANK:
        assert 3 <= len(q["options"]) <= 6
        assert len(set(q["options"])) == len(q["options"]), q["id"]
        assert 0 <= q["answer"] < len(q["options"]), q["id"]
        assert q["explanation"].strip()
        assert q["difficulty"] in {"easy", "medium", "hard"}


def test_every_category_has_questions():
    assert set(get_categories()) == {"technical", "aptitude", "communication", "personal"}
    for c in get_categories():
        assert len(get_questions(category=c)) >= 4


def test_correct_wrong_and_skipped():
    q = QUESTION_BANK[0]
    assert evaluate_answer(q["answer"], q)["score"] == 100
    wrong = (q["answer"] + 1) % len(q["options"])
    r = evaluate_answer(wrong, q)
    assert r["score"] == 0 and not r["correct"] and r["answered"]
    s = evaluate_answer(None, q)
    assert s["score"] == 0 and not s["answered"]
    assert evaluate_answer(99, q)["answered"] is False   # out-of-range ignored


def test_shuffle_keeps_correct_answer_correct():
    originals = {q["id"]: q["options"][q["answer"]] for q in QUESTION_BANK}
    for seed in range(20):
        s = InterviewSession(num_questions=10, seed=seed)
        for q in s.questions:
            assert q["options"][q["answer"]] == originals[q["id"]]


def test_first_answer_counts():
    s = InterviewSession(num_questions=3, seed=1)
    q = s.get_question(0)
    s.submit_answer(0, q["answer"])
    s.submit_answer(0, (q["answer"] + 1) % len(q["options"]))   # retry ignored
    assert s.results[0]["correct"]


def test_summary_counts_unanswered_as_zero():
    s = InterviewSession(num_questions=4, seed=2)
    s.submit_answer(0, s.get_question(0)["answer"])
    sm = s.finish()
    assert sm["correct"] == 1 and sm["total"] == 4 and sm["overall_score"] == 25.0


def test_num_questions_is_clamped():
    assert InterviewSession(category="aptitude", num_questions=999).total_questions() == len(get_questions("aptitude"))


def test_web_flow():
    flask = pytest.importorskip("flask")
    import web_app
    c = web_app.app.test_client()
    assert c.post("/start", data={"category": "aptitude", "num_questions": "abc"}).status_code == 302
    r = c.get("/question"); assert b'type="radio"' in r.data
    r = c.post("/answer", data={}, follow_redirects=True)
    assert b"Please select an option" in r.data
    r = c.post("/answer", data={"choice": "0"}); assert b"explanation" in r.data
    assert c.post("/next").status_code == 302
