"""
AI Interview Practice Bot -- Desktop App (Tkinter)

Run with:
    python desktop_app.py

Shares the same core scoring/session engine as web_app.py -- only the
UI layer differs, per the "dual deployment" design in the project deck.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from core.questions import get_categories, CATEGORY_LABELS
from core.session import InterviewSession


class InterviewBotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Interview Practice Bot")
        self.geometry("720x560")
        self.minsize(640, 500)
        self.configure(bg="#f4f6f8")

        self.session = None
        self.current_index = 0

        self._build_start_screen()

    # ------------------------------------------------------------------ #
    # Screen 1: choose a category and start
    # ------------------------------------------------------------------ #
    def _build_start_screen(self):
        self._clear()
        frame = ttk.Frame(self, padding=30)
        frame.pack(expand=True, fill="both")

        ttk.Label(
            frame, text="AI Interview Practice Bot",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(10, 4))
        ttk.Label(
            frame,
            text="Practice technical, aptitude, communication, and personal\n"
                 "interview questions as multiple-choice, with instant feedback.",
            font=("Segoe UI", 11), justify="center"
        ).pack(pady=(0, 24))

        ttk.Label(frame, text="Choose a category:", font=("Segoe UI", 12)).pack(pady=(0, 6))

        self.category_var = tk.StringVar(value="all")
        categories = ["all"] + get_categories()
        for cat in categories:
            label = "All categories (mixed)" if cat == "all" else CATEGORY_LABELS.get(cat, cat)
            ttk.Radiobutton(
                frame, text=label, value=cat, variable=self.category_var
            ).pack(anchor="w", padx=80)

        ttk.Label(frame, text="Number of questions:", font=("Segoe UI", 12)).pack(pady=(16, 6))
        self.num_q_var = tk.IntVar(value=5)
        ttk.Spinbox(frame, from_=3, to=10, textvariable=self.num_q_var, width=5).pack()

        ttk.Button(
            frame, text="Start Practice Session", command=self._start_session
        ).pack(pady=28)

    def _start_session(self):
        category = None if self.category_var.get() == "all" else self.category_var.get()
        self.session = InterviewSession(
            category=category, num_questions=self.num_q_var.get()
        )
        self.current_index = 0
        self._build_question_screen()

    # ------------------------------------------------------------------ #
    # Screen 2: answer questions one at a time
    # ------------------------------------------------------------------ #
    def _build_question_screen(self):
        self._clear()
        question = self.session.get_question(self.current_index)

        frame = ttk.Frame(self, padding=24)
        frame.pack(expand=True, fill="both")

        progress = f"Question {self.current_index + 1} of {self.session.total_questions()}"
        ttk.Label(frame, text=progress, font=("Segoe UI", 10, "italic")).pack(anchor="w")
        ttk.Label(
            frame, text=CATEGORY_LABELS.get(question["category"], question["category"]),
            font=("Segoe UI", 10, "bold"), foreground="#2563eb"
        ).pack(anchor="w", pady=(2, 10))

        ttk.Label(
            frame, text=question["text"], font=("Segoe UI", 14),
            wraplength=650, justify="left"
        ).pack(anchor="w", pady=(0, 14))

        self.choice_var = tk.IntVar(value=-1)
        for i, opt in enumerate(question["options"]):
            ttk.Radiobutton(
                frame, text=opt, value=i, variable=self.choice_var
            ).pack(anchor="w", pady=4)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", side="bottom")
        ttk.Button(btn_frame, text="Submit Answer", command=self._submit_answer).pack(side="right")

    def _submit_answer(self):
        selected = self.choice_var.get()
        if selected < 0:
            messagebox.showinfo("Select an option", "Please choose an answer before submitting.")
            return
        result = self.session.submit_answer(self.current_index, selected)
        self._build_feedback_screen(result)

    # ------------------------------------------------------------------ #
    # Screen 3: instant feedback for that answer
    # ------------------------------------------------------------------ #
    def _build_feedback_screen(self, result):
        self._clear()
        frame = ttk.Frame(self, padding=24)
        frame.pack(expand=True, fill="both")

        ok = result["correct"]
        ttk.Label(
            frame, text="Correct!" if ok else "Not quite.",
            font=("Segoe UI", 18, "bold"),
            foreground="#16a34a" if ok else "#dc2626"
        ).pack(anchor="w", pady=(0, 10))

        if not ok:
            ttk.Label(frame, text=f"Your answer: {result['selected_text'] or '(none)'}",
                      font=("Segoe UI", 11), wraplength=650, justify="left").pack(anchor="w", pady=2)
            ttk.Label(frame, text=f"Correct answer: {result['correct_text']}",
                      font=("Segoe UI", 11, "bold"), wraplength=650, justify="left").pack(anchor="w", pady=2)
        ttk.Label(frame, text=result["explanation"], font=("Segoe UI", 11),
                  wraplength=650, justify="left").pack(anchor="w", pady=(12, 2))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(24, 0))

        is_last = self.current_index + 1 >= self.session.total_questions()
        label = "See Session Summary" if is_last else "Next Question"
        ttk.Button(btn_frame, text=label, command=self._advance).pack(side="right")

    def _advance(self):
        self.current_index += 1
        if self.current_index >= self.session.total_questions():
            self._build_summary_screen()
        else:
            self._build_question_screen()

    # ------------------------------------------------------------------ #
    # Screen 4: end-of-session summary
    # ------------------------------------------------------------------ #
    def _build_summary_screen(self):
        self._clear()
        summary = self.session.finish()

        frame = ttk.Frame(self, padding=24)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Session Summary", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(
            frame, text=f"Score: {summary['correct']} / {summary['total']}  ({summary['overall_score']}%)",
            font=("Segoe UI", 14)
        ).pack(anchor="w", pady=(6, 14))

        ttk.Label(frame, text="Category breakdown:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        for cat, d in summary["category_breakdown"].items():
            ttk.Label(frame, text=f"  {cat}: {d['correct']} / {d['total']} ({d['percent']}%)").pack(anchor="w")

        ttk.Label(frame, text="\nStrengths:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        for s in summary["strengths"]:
            ttk.Label(frame, text=f"  \u2022 {s}", wraplength=650, justify="left").pack(anchor="w")

        ttk.Label(frame, text="\nAreas to improve:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        for s in summary["improvement_areas"]:
            ttk.Label(frame, text=f"  \u2022 {s}", wraplength=650, justify="left").pack(anchor="w")

        ttk.Button(frame, text="Practice Again", command=self._build_start_screen).pack(pady=24)

    # ------------------------------------------------------------------ #
    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = InterviewBotApp()
    app.mainloop()
