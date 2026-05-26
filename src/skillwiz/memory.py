import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List


def _memory_path() -> Path:
    return Path(os.getenv("SKILLWIZ_MEMORY_PATH", "data/memory.json"))


@dataclass
class MemoryEntry:
    user: str
    assistant: str
    timestamp: str


class ConversationMemory:
    def __init__(self) -> None:
        self.path = _memory_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[MemoryEntry]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [MemoryEntry(**item) for item in data]

    def append(self, entry: MemoryEntry) -> None:
        data = [item.__dict__ for item in self.load()]
        data.append(entry.__dict__)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def recent(self, limit: int = 5) -> List[MemoryEntry]:
        items = self.load()
        return items[-limit:]
