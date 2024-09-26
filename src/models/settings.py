from dataclasses import asdict, dataclass
from src.data.genres import GENRES

from src.models.music import GenreName


@dataclass(frozen=True)
class Settings:
    incognito: bool
    genre_explo_ratio: float
    genre_subgenre_ratio: float
    genre_weights: dict[GenreName, int]

    def to_dict(self) -> dict:

        data = asdict(self)
        data['genre_weights'] = {k.value: v for k, v in self.genre_weights.items()}
        return data
    
    def from_dict(data: dict):

        data['genre_weights'] = {GenreName(k): v for k, v in data['genre_weights'].items()}
        return Settings(**data)
    

    def show_genre_reparition(self) -> tuple[dict[str, int], str]:

        total = sum(self.genre_weights.values())
        genre_proportion = {k.value: v/total*100 for k, v in self.genre_weights.items()}

        genre_repartition = '\n'.join([
            f'- **{g.name.value}**:         {self.genre_weights[g.name]} -> *({round(genre_proportion[g.name.value], 1)}%)*' 
            for g in GENRES 
        ])

        return genre_proportion, f'**Genre proportions** \n\n{genre_repartition}'
    

    def show_settings(self) -> str:

        intro = '**Current settings:**'
        incognito = f"- Incognito mode: **{'Activated' if self.incognito else 'Deactivated'}**"
        challenge_ratio = f'- Genre Exploration Ratio: **{self.genre_explo_ratio*100}%**'
        genre_subgenre_ratio = f'- Genre / Subgenre Ratio: **{self.genre_subgenre_ratio*100}%**'

        genre_prop, _ = self.show_genre_reparition()
        genre_prop = ' - '.join([f'{g} ({round(p, 1)}%)' for (g, p) in genre_prop.items()])
        genre_proportion = f'- Genre Proportions: {genre_prop}'

        explanations = '**Info:**' + \
            '\n- The incognito mode is a mode where contributions are submitted privately to the bot. ' + \
            '`!settings_incognito <0/1>`' + \
            '\n- The genre exploration ratio determines the probability of a genre being selected over a challenge. ' + \
            '`!settings_ger <ratio>`' + \
            '\n- The genre / subgenre ratio determines the probability of a genre being selected over a subgenre. ' + \
            '`!settings_gsr <ratio>`' + \
            '\n- The genre proportions determine the probability of a genre being selected. ' + \
            '`!settings_gpr <genre> <weight>`' 

        return f'{intro}\n{incognito}\n{challenge_ratio}\n{genre_subgenre_ratio}\n{genre_proportion}\n\n{explanations}'

    

DEFAULT_SETTINGS = Settings(
    incognito=False,
    genre_explo_ratio=0.5,
    genre_subgenre_ratio=0.9,
    genre_weights={
        GenreName.ROCK : 2,
        GenreName.POP : 1,
        GenreName.FUNKSOUL: 1,
        GenreName.ELECTRONIC : 3,
        GenreName.JAZZ : 1,
        GenreName.HIPHOP : 1,
        GenreName.CLASSICAL : 1,
        GenreName.REGGAE : 1,
        GenreName.HOUSE : 5,
        GenreName.TECHNO : 2,
        GenreName.DISCO : 1,
        GenreName.WORLD : 1,
        GenreName.ANY : 1,
    }
)









