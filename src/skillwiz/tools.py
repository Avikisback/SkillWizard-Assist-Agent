from typing import Optional

from .db import get_student_progress
from .models import StudentProgress


def fetch_progress(user_id: str) -> StudentProgress:
    progress = get_student_progress(user_id)
    if not progress:
        raise ValueError(f"No progress found for user_id={user_id}")
    return progress


def _rule_based_plan(progress: StudentProgress) -> str:
    if progress.pending_topics:
        next_topic = progress.pending_topics[0]
        return (
            f"Study '{next_topic}' next. It builds on {progress.completed_topics[-1]}"
            " and keeps momentum in your current phase."
        )
    if progress.completed_topics:
        return (
            "Most topics are complete. Do a short review and build a mini project"
            " to practice the concepts."
        )
    return "Start by listing a few core topics for your target and pick one to begin."


def suggest_next_step(
    progress: StudentProgress,
    question: str,
    llm: Optional[object] = None,
    history: Optional[str] = None,
) -> str:
    plan = _rule_based_plan(progress)
    prompt = (
        "You are a study coach. Provide a concise, actionable response. "
        "Reference the student's current phase and streak.\n\n"
        f"Question: {question}\n"
        f"Target: {progress.target}\n"
        f"Current phase: {progress.current_phase}\n"
        f"Completed topics: {', '.join(progress.completed_topics)}\n"
        f"Pending topics: {', '.join(progress.pending_topics)}\n"
        f"Streak: {progress.streak}\n"
        f"Suggested plan: {plan}\n"
    )
    if history:
        prompt += f"Recent context:\n{history}\n"
    if llm:
        try:
            response = llm.invoke(prompt)
            return response.content.strip()
        except Exception:
            return _fallback_response(progress, plan)
    return _fallback_response(progress, plan)


def _fallback_response(progress: StudentProgress, plan: str) -> str:
    return (
        f"You are in '{progress.current_phase}' with a {progress.streak}-day streak. "
        f"{plan}"
    )
