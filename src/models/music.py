from dataclasses import asdict, dataclass
from typing import Literal, Union
from enum import Enum


class GenreName(Enum):
    ROCK = "Rock"
    POP = "Pop"
    RAP = "Rap"
    JAZZ = "Jazz"
    CLASSICAL = "Classical"
    ELECTRONIC = "Electronic"
    REGGAE = "Reggae"
    HOUSE = "House"
    TECHNO = "Techno"
    DISCO = "Disco"
    FOLK = "Folk"
    ANY = "Any"


@dataclass(frozen=True)
class Genre:
    name: GenreName
    description: str
    weight: int = 1 

    def to_dict(self):
        data = asdict(self)
        data['name'] = self.name.value

    def from_dict(data):
        data['name'] = GenreName(data['name'])
        return Genre(**data)


@dataclass(frozen=True)
class SubGenre:
    name: str
    genre: Genre
    description: str

    def to_dict(self):
        data = asdict(self)
        data['genre'] = self.genre.to_dict()
        return data


@dataclass(frozen=True)
class Challenge:
    name: str
    description: str

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Theme:
    type: Literal['Genre', 'SubGenre', 'Challenge']
    content: Union[Genre, SubGenre, Challenge]

    def to_dict(self) -> dict:
        data = asdict(self)
        data['content'] = self.content.to_dict()
        return data
    
    def from_dict(data: dict):
        content = data['content']
        if 'genre' in content:
            content['genre'] = Genre.from_dict(content['genre'])
        return Theme(**data)


@dataclass(frozen=True)
class Artist:
    name: str
    genre: Genre


@dataclass(frozen=True)
class Track:
    title: str
    artist: Artist
    genre: Genre