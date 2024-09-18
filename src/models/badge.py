from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional 


@dataclass(frozen=True)
class Badge:
    name: str
    description: str
    emoji: str
    metal: Optional[Literal['Gold', 'Silver', 'Bronze', 'Platinum']] = None

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'emoji': self.emoji,
            'metal': self.metal
        }

    def from_dict(data: dict):
        return Badge(**data)
