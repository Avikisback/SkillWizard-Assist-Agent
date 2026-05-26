from skillwiz.models import StudentProgress
from skillwiz.tools import suggest_next_step


def test_suggest_next_step_rule_based():
    progress = StudentProgress(
        user_id="user_123",
        target="Frontend Developer",
        current_phase="JavaScript Basics",
        completed_topics=["Variables"],
        pending_topics=["Loops"],
        streak=3,
    )
    response = suggest_next_step(progress, "What should I do today?", llm=None)
    assert "Loops" in response or "JavaScript Basics" in response
