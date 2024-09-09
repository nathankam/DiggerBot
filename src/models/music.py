from dataclasses import dataclass
from typing import Literal, Union 

@dataclass(frozen=True)
class Genre:
    name: str
    description: str
    weight: int = 1 


@dataclass(frozen=True)
class SubGenre:
    name: str
    genre: Genre
    description: str


@dataclass(frozen=True)
class Challenge:
    name: str
    description: str


@dataclass(frozen=True)
class Theme:
    type: Literal['Genre', 'SubGenre', 'Challenge']
    content: Union[Genre, SubGenre, Challenge]


@dataclass(frozen=True)
class Artist:
    name: str
    genre: Genre


@dataclass(frozen=True)
class Track:
    title: str
    artist: Artist
    genre: Genre