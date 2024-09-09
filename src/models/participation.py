from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Participation:
    id: int
    user: str
    link: str
    platform: Literal['SPOTIFY', 'YOUTUBE']
    date: str
    