"""
Scoring for multiple-choice questions.

Answers are checked exactly, so scores are deterministic -- no NLP
guesswork. The decoupled design is unchanged: both UIs call
`evaluate_answer()` and render the returned dict.
"""


def evaluate_answer(selected_index, question):
    """
    `question` is a (possibly option-shuffled) dict from the question bank.
    `selected_index` is the index chosen in question["options"], or None
    if the candidate skipped.
    """
    options = question["options"]
    correct_index = question["answer"]
    answered = selected_index is not None and 0 <= selected_index < len(options)
    correct = answered and selected_index == correct_index

    if not answered:
        feedback = "No option was selected, so this question scores 0."
    elif correct:
        feedback = "Correct!"
    else:
        feedback = "Not quite."

    return {
        "question_id": question["id"],
        "category": question["category"],
        "answered": answered,
        "correct": correct,
        "score": 100.0 if correct else 0.0,
        "selected_text": options[selected_index] if answered else None,
        "correct_text": options[correct_index],
        "explanation": question["explanation"],
        "feedback": [feedback],
    }
