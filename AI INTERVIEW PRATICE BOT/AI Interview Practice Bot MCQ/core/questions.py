"""
Fixed multiple-choice question bank for the AI Interview Practice Bot.

Each question:
    id            unique string id
    category      technical | aptitude | communication | personal
    difficulty    easy | medium | hard
    text          the question shown to the candidate
    options       list of answer choices (shown in shuffled order)
    answer        index into `options` of the correct choice
    explanation   shown after answering

To add a question, append a dict to QUESTION_BANK -- nothing else changes.
"""

QUESTION_BANK = [
    # ------------------------------ TECHNICAL ------------------------------ #
    {"id": "tech_01", "category": "technical", "difficulty": "easy",
     "text": "What is the key difference between a list and a tuple in Python?",
     "options": ["Lists are mutable; tuples are immutable",
                 "Lists are immutable; tuples are mutable",
                 "Lists can only hold numbers; tuples hold any type",
                 "There is no difference"],
     "answer": 0,
     "explanation": "Lists can be changed after creation; tuples cannot. Because of this, tuples are hashable and can be dictionary keys."},
    {"id": "tech_02", "category": "technical", "difficulty": "medium",
     "text": "Why are hash table lookups O(1) on average?",
     "options": ["Keys are always stored in sorted order",
                 "The hash function computes the storage index directly",
                 "Every lookup uses binary search",
                 "Values are cached in the CPU"],
     "answer": 1,
     "explanation": "The hash of the key maps straight to an array index, so no sequential search is needed. Collisions can degrade the worst case to O(n)."},
    {"id": "tech_03", "category": "technical", "difficulty": "medium",
     "text": "Which task is an example of unsupervised learning?",
     "options": ["Predicting house prices from labeled sales data",
                 "Classifying emails as spam or not spam",
                 "Grouping customers into segments without predefined labels",
                 "Recognizing handwritten digits with known labels"],
     "answer": 2,
     "explanation": "Clustering finds structure in unlabeled data. The other options all learn from labeled examples."},
    {"id": "tech_04", "category": "technical", "difficulty": "medium",
     "text": "What does SQL's JOIN clause do?",
     "options": ["Deletes duplicate rows from a table",
                 "Combines rows from two or more tables based on a related column",
                 "Sorts the result set",
                 "Creates an index on a column"],
     "answer": 1,
     "explanation": "JOIN merges rows from multiple tables using a matching condition, usually a foreign key."},
    {"id": "tech_05", "category": "technical", "difficulty": "hard",
     "text": "A model scores 99% on training data but 70% on test data. What is the most likely problem?",
     "options": ["Underfitting", "Data leakage from the test set into training",
                 "Overfitting", "Too few features were removed"],
     "answer": 2,
     "explanation": "A large gap between training and test performance indicates overfitting: the model memorized training data instead of generalizing."},
    {"id": "tech_06", "category": "technical", "difficulty": "easy",
     "text": "Which HTTP method is normally used to retrieve data without changing it?",
     "options": ["POST", "PUT", "DELETE", "GET"],
     "answer": 3,
     "explanation": "GET is safe and idempotent: it reads a resource without modifying it."},

    # ------------------------------ APTITUDE ------------------------------- #
    {"id": "apt_01", "category": "aptitude", "difficulty": "easy",
     "text": "What comes next in the series: 2, 6, 12, 20, 30, ?",
     "options": ["38", "40", "42", "44"],
     "answer": 2,
     "explanation": "Differences grow by 2 each time (4, 6, 8, 10, 12). 30 + 12 = 42."},
    {"id": "apt_02", "category": "aptitude", "difficulty": "easy",
     "text": "A train travels 360 km in 4 hours. At the same speed, how far does it travel in 7 hours?",
     "options": ["560 km", "600 km", "630 km", "720 km"],
     "answer": 2,
     "explanation": "Speed = 360 / 4 = 90 km/h. Distance in 7 hours = 90 x 7 = 630 km."},
    {"id": "apt_03", "category": "aptitude", "difficulty": "medium",
     "text": "If the price of an item rises by 20% and then falls by 20%, the final price compared to the original is:",
     "options": ["Unchanged", "4% lower", "4% higher", "2% lower"],
     "answer": 1,
     "explanation": "1.2 x 0.8 = 0.96, so the final price is 96% of the original, a 4% decrease."},
    {"id": "apt_04", "category": "aptitude", "difficulty": "medium",
     "text": "All managers are employees. Some employees are engineers. Which conclusion must be true?",
     "options": ["All engineers are managers", "Some managers are engineers",
                 "All managers are engineers", "None of these must be true"],
     "answer": 3,
     "explanation": "The statements don't say the 'some employees' who are engineers overlap with managers, so no other conclusion is guaranteed."},
    {"id": "apt_05", "category": "aptitude", "difficulty": "hard",
     "text": "A can finish a job in 12 days and B in 6 days. Working together, how many days do they need?",
     "options": ["3", "4", "5", "9"],
     "answer": 1,
     "explanation": "Combined rate = 1/12 + 1/6 = 3/12 = 1/4 job per day, so 4 days."},

    # ---------------------------- COMMUNICATION ---------------------------- #
    {"id": "comm_01", "category": "communication", "difficulty": "easy",
     "text": "A teammate is explaining a problem and you disagree. What is the best first step?",
     "options": ["Interrupt to correct them immediately",
                 "Let them finish, then restate their point to confirm understanding",
                 "Stay silent and ignore it",
                 "Escalate to your manager"],
     "answer": 1,
     "explanation": "Active listening and confirming understanding prevents misunderstandings before you share your own view."},
    {"id": "comm_02", "category": "communication", "difficulty": "medium",
     "text": "You must explain a technical concept to a non-technical stakeholder. Which approach works best?",
     "options": ["Use precise jargon so nothing is lost",
                 "Send detailed documentation and avoid a conversation",
                 "Use plain language and an analogy tied to their goals",
                 "Keep it as short as possible, whatever it leaves out"],
     "answer": 2,
     "explanation": "Adapt to your audience: plain language and relevant analogies make the message actionable."},
    {"id": "comm_03", "category": "communication", "difficulty": "medium",
     "text": "You realize you will miss a deadline. What should you do?",
     "options": ["Wait until the deadline passes, then explain",
                 "Tell stakeholders early, explain the cause, and propose a new date",
                 "Rush and submit lower-quality work without saying anything",
                 "Ask a colleague to inform the team"],
     "answer": 1,
     "explanation": "Early, honest communication with a concrete plan preserves trust and lets others adjust."},
    {"id": "comm_04", "category": "communication", "difficulty": "hard",
     "text": "Which is the most constructive way to give critical feedback to a colleague?",
     "options": ["\"You always make mistakes like this.\"",
                 "Give it publicly so everyone learns",
                 "Describe the specific behavior and its impact, then suggest an improvement, in private",
                 "Hint at it indirectly and hope they notice"],
     "answer": 2,
     "explanation": "Specific, behavior-focused, private feedback with a path forward is easiest to accept and act on."},

    # ------------------------------ PERSONAL ------------------------------- #
    {"id": "pers_01", "category": "personal", "difficulty": "easy",
     "text": "When asked \"Tell me about yourself\" in an interview, the best answer is:",
     "options": ["A full life story from childhood",
                 "A short summary of your relevant background, skills, and goals for the role",
                 "A list of your hobbies",
                 "\"It's all on my resume.\""],
     "answer": 1,
     "explanation": "Keep it concise and relevant: present, past, and future tied to the role."},
    {"id": "pers_02", "category": "personal", "difficulty": "medium",
     "text": "Asked about a weakness, which response is strongest?",
     "options": ["\"I'm a perfectionist.\"",
                 "\"I don't really have any.\"",
                 "A real, non-critical weakness plus concrete steps you are taking to improve it",
                 "A weakness that is essential to the job"],
     "answer": 2,
     "explanation": "Honest self-awareness plus evidence of improvement is more credible than a cliche or a denial."},
    {"id": "pers_03", "category": "personal", "difficulty": "medium",
     "text": "\"Why do you want to work for this company?\" Which answer is best?",
     "options": ["\"It pays well and is close to home.\"",
                 "\"I need a job.\"",
                 "Connect specific things about the company's mission or products to your skills and what you'd contribute",
                 "\"Everyone says it's a great place.\""],
     "answer": 2,
     "explanation": "Specific, researched reasons show genuine interest and fit."},
    {"id": "pers_04", "category": "personal", "difficulty": "hard",
     "text": "Describe a failure: which structure makes for the strongest answer?",
     "options": ["Blame the circumstances so it isn't your fault",
                 "Say you've never really failed",
                 "Situation, your role, what went wrong, what you learned, and what you changed afterwards",
                 "Give a very long story without a conclusion"],
     "answer": 2,
     "explanation": "Owning the mistake and showing the lesson and change demonstrates growth."},
]


def get_categories():
    seen = []
    for q in QUESTION_BANK:
        if q["category"] not in seen:
            seen.append(q["category"])
    return seen


def get_questions(category=None, difficulty=None):
    result = QUESTION_BANK
    if category:
        result = [q for q in result if q["category"] == category]
    if difficulty:
        result = [q for q in result if q["difficulty"] == difficulty]
    return list(result)


def get_question_by_id(question_id):
    for q in QUESTION_BANK:
        if q["id"] == question_id:
            return q
    return None


CATEGORY_LABELS = {
    "technical": "Technical",
    "aptitude": "Aptitude",
    "communication": "Communication",
    "personal": "Personal / Background",
}
