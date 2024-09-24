from src.models.message import React

REACTS = [
    React(
        name='COUPDECOEUR',
        emoji="🌟",
        meaning="Coup de coeur",
        points=300,
    ),
    React(
        name="VOTE",
        emoji="🪩",
        meaning="Vote",
        points=200,
    ),
    React(
        name="FIND",
        emoji="💣",
        meaning="Good Find",
        points=100,
    )
]