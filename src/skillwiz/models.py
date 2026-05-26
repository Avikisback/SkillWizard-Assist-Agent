from typing import List

from pydantic import BaseModel


class StudentProgress(BaseModel):
    user_id: str
    target: str
    current_phase: str
    completed_topics: List[str]
    pending_topics: List[str]
    streak: int
