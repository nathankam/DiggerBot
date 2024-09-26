from src.models.message import React

REACTS = [
    React(
        name='TUNE',
        emoji="💣",
        meaning={
            'EN': "Special react for really special tracks!",
            'FR': "Réact spécial pour tracks vraiment spéciales!"
        }
    ),
    React(
        name="DIGGER",
        emoji="🧐",
        meaning={
            'EN': "But where did you even find this?",
            'FR': "Mais ou est ce que tu vas chercher ça?"
        }
    )
]