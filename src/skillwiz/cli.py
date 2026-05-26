import argparse
from datetime import datetime

from dotenv import load_dotenv

from .llm import get_llm
from .memory import ConversationMemory, MemoryEntry
from .tools import fetch_progress, suggest_next_step


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SkillWiz AI agent")
    parser.add_argument("--user-id", default="user_123", help="Student user id")
    parser.add_argument("--question", help="User question")
    return parser.parse_args()


def _format_history(entries: list[MemoryEntry]) -> str | None:
    if not entries:
        return None
    lines: list[str] = []
    for item in entries:
        lines.append(f"User: {item.user}")
        lines.append(f"Assistant: {item.assistant}")
    return "\n".join(lines)


def main() -> None:
    load_dotenv()
    args = _parse_args()
    question = args.question or input("What should I do today? ")

    memory = ConversationMemory()
    llm = get_llm()

    history = _format_history(memory.recent())

    progress = fetch_progress(args.user_id)
    response = suggest_next_step(progress, question, llm, history=history)

    memory.append(
        MemoryEntry(
            user=question,
            assistant=response,
            timestamp=datetime.utcnow().isoformat(),
        )
    )

    print(response)
