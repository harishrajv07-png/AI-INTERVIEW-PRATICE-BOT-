"""
Session management: picks fixed questions, shuffles their options,
scores each answer, and builds the end-of-session summary.
"""

import copy
import random
from datetime import datetime

from core.questions import get_questions, CATEGORY_LABELS
from core.scoring import evaluate_answer


class InterviewSession:
    def __init__(self, category=None, difficulty=None, num_questions=5, seed=None):
        rng = random.Random(seed)
        pool = get_questions(category=category, difficulty=difficulty) or get_questions()
        rng.shuffle(pool)
        num_questions = max(1, min(int(num_questions), len(pool)))

        self.questions = [self._shuffle_options(q, rng) for q in pool[:num_questions]]
        self.category = category
        self.results = {}          # index -> result dict (one answer per question)
        self.started_at = datetime.now()
        self.finished_at = None

    @staticmethod
    def _shuffle_options(question, rng):
        q = copy.deepcopy(question)
        correct_text = q["options"][q["answer"]]
        rng.shuffle(q["options"])
        q["answer"] = q["options"].index(correct_text)
        return q

    # ------------------------------------------------------------------ #
    def total_questions(self):
        return len(self.questions)

    def get_question(self, index):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None

    def is_answered(self, index):
        return index in self.results

    def submit_answer(self, index, selected_index):
        """Score one answer. Re-submitting the same question is ignored
        (first answer counts) so refreshing/back-button can't change a score."""
        question = self.get_question(index)
        if question is None:
            raise IndexError("No question at that index.")
        if index in self.results:
            return self.results[index]

        result = evaluate_answer(selected_index, question)
        result["question_text"] = question["text"]
        self.results[index] = result
        return result

    def is_complete(self):
        return len(self.results) >= len(self.questions)

    def finish(self):
        if self.finished_at is None:
            self.finished_at = datetime.now()
        return self.build_summary()

    # ------------------------------------------------------------------ #
    def build_summary(self):
        results = [self.results[i] for i in sorted(self.results)]
        total = len(self.questions)
        if not results:
            return {"overall_score": 0, "correct": 0, "answered": 0, "total": total,
                    "category_breakdown": {}, "strengths": [], "improvement_areas": [],
                    "review": [], "started_at": self.started_at.strftime("%Y-%m-%d %H:%M")}

        correct = sum(r["correct"] for r in results)
        overall = round(correct / total * 100, 1)   # unanswered count as 0

        by_cat = {}
        for r in results:
            by_cat.setdefault(r["category"], []).append(r["correct"])
        breakdown = {
            CATEGORY_LABELS.get(c, c): {"correct": sum(v), "total": len(v),
                                         "percent": round(sum(v) / len(v) * 100)}
            for c, v in by_cat.items()
        }

        strengths = [f"{lbl}: {d['correct']}/{d['total']} correct"
                     for lbl, d in breakdown.items() if d["percent"] >= 70]
        improve = [f"{lbl}: {d['correct']}/{d['total']} correct -- review these topics"
                   for lbl, d in breakdown.items() if d["percent"] < 50]
        if not strengths:
            strengths = ["No category reached 70% yet -- keep practicing."]
        if not improve:
            improve = ["No major weak spots -- solid session overall."]

        review = [r for r in results if not r["correct"]]
        return {
            "overall_score": overall, "correct": correct, "answered": len(results),
            "total": total, "category_breakdown": breakdown,
            "strengths": strengths, "improvement_areas": improve, "review": review,
            "started_at": self.started_at.strftime("%Y-%m-%d %H:%M"),
        }
