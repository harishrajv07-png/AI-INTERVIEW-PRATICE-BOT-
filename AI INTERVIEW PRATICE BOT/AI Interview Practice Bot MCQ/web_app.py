"""
AI Interview Practice Bot -- Web App (Flask), multiple-choice edition.

Run with:  python web_app.py   then open http://127.0.0.1:5000

Sessions live server-side in memory (fine for single-user practice use).
Set SECRET_KEY in the environment to keep browser sessions valid across
restarts; set FLASK_DEBUG=1 for debug mode.
"""

import os
import secrets
import time

from flask import (Flask, render_template, request, redirect, url_for,
                   session as flask_session)

from core.questions import get_categories, CATEGORY_LABELS
from core.session import InterviewSession

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(16)

ACTIVE_SESSIONS = {}          # { session_id: (InterviewSession, last_used_ts) }
SESSION_TTL = 2 * 60 * 60     # drop sessions idle for 2 hours


def _purge_old_sessions():
    cutoff = time.time() - SESSION_TTL
    for sid in [s for s, (_, ts) in ACTIVE_SESSIONS.items() if ts < cutoff]:
        del ACTIVE_SESSIONS[sid]


def _get_session():
    entry = ACTIVE_SESSIONS.get(flask_session.get("session_id"))
    if entry is None:
        return None
    ACTIVE_SESSIONS[flask_session["session_id"]] = (entry[0], time.time())
    return entry[0]


@app.route("/")
def index():
    return render_template("index.html", categories=get_categories(),
                           labels=CATEGORY_LABELS)


@app.route("/start", methods=["POST"])
def start():
    _purge_old_sessions()
    category = request.form.get("category") or None
    if category not in get_categories():
        category = None
    try:
        num_questions = int(request.form.get("num_questions", 5))
    except ValueError:
        num_questions = 5
    num_questions = max(3, min(num_questions, 10))

    sid = secrets.token_hex(8)
    ACTIVE_SESSIONS[sid] = (InterviewSession(category=category,
                                             num_questions=num_questions), time.time())
    flask_session["session_id"] = sid
    flask_session["index"] = 0
    return redirect(url_for("question"))


@app.route("/question")
def question():
    s = _get_session()
    if s is None:
        return redirect(url_for("index"))
    index = flask_session.get("index", 0)
    q = s.get_question(index)
    if q is None:
        return redirect(url_for("summary"))
    if s.is_answered(index):               # back button after answering
        return render_template("feedback.html", **_feedback_ctx(s, index))
    return render_template("interview.html", question=q, index=index,
                           total=s.total_questions(),
                           category_label=CATEGORY_LABELS.get(q["category"], q["category"]),
                           error=request.args.get("error"))


def _feedback_ctx(s, index):
    return dict(result=s.results[index], question=s.get_question(index),
                index=index, total=s.total_questions(),
                is_last=(index + 1 >= s.total_questions()))


@app.route("/answer", methods=["POST"])
def answer():
    s = _get_session()
    if s is None:
        return redirect(url_for("index"))
    index = flask_session.get("index", 0)
    if s.get_question(index) is None:
        return redirect(url_for("summary"))

    choice = request.form.get("choice")
    if not s.is_answered(index):
        try:
            selected = int(choice)
        except (TypeError, ValueError):
            return redirect(url_for("question", error="Please select an option."))
        if not 0 <= selected < len(s.get_question(index)["options"]):
            return redirect(url_for("question", error="Please select an option."))
        s.submit_answer(index, selected)
    return render_template("feedback.html", **_feedback_ctx(s, index))


@app.route("/next", methods=["POST"])
def next_question():
    s = _get_session()
    if s is None:
        return redirect(url_for("index"))
    index = flask_session.get("index", 0)
    if s.is_answered(index):               # can't skip ahead without answering
        flask_session["index"] = index + 1
    return redirect(url_for("question"))


@app.route("/summary")
def summary():
    s = _get_session()
    if s is None:
        return redirect(url_for("index"))
    return render_template("summary.html", summary=s.finish())


@app.route("/restart")
def restart():
    ACTIVE_SESSIONS.pop(flask_session.get("session_id"), None)
    flask_session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
