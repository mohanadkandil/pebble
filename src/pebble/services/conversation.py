import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, field, asdict

DATA_DIR = Path(__file__).parent.parent / "data"  

@dataclass
class Message: 
    role: str
    content: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat)

class ConversationLog:
    def __init__(self, filename: str = "conversation.json"):
        DATA_DIR.mkdir(parent=True, exist_ok=True)
        self.filepath = DATA_DIR / filename
        self.messages: List[Message] = []
        self._load()

    def _load(self):
        if self.filepath.exists():
            with open(self.filepath, "r") as f:
                data = json.load(f)
            self.messages = [Message(**msg) for msg in data]
    
    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump([asdict(msg) for msg in self.messages], f, indent=2)

    def add_user_message(self, content: str):
        self.messages.append(Message(role="user", content=content))
        self._save()

    def add_assistant_message(self, content: str):
          self.messages.append(Message(role="assistant", content=content))
          self._save()
    
    def add_agent_message(self, content: str):
        self.messages.append(Message(role="agent", content=content))
        self._save()

    def get_history(self, limit: int = 20) -> List[Dict]:
        recent = self.messages[-limit:]
        result = []
        for m in recent:
              role = "user" if m.role == "agent" else m.role
              result.append({"role": role, "content": m.content})
        return result

    def get_all(self) -> List[Dict]:
        return [asdict(m) for m in self.messages]

    def clear(self):
        self.messages = []
        self._save()

_conversation_log = None 

def get_conversation_log() -> ConversationLog:
    global _conversation_log
    if not _conversation_log:
        _conversation_log = ConversationLog()
    return _conversation_log


    

