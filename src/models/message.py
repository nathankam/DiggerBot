from dataclasses import dataclass
from enum import Enum
from typing import Optional 

@dataclass(frozen=True)
class TextMessage:
    text: str



@dataclass(frozen=True)
class Command: 
    name: str
    code: str
    description: str
    instructions: Optional[str] = None
    restricted: bool = False


@dataclass(frozen=True)
class React:
    name: str
    emoji: str
    meaning: str




