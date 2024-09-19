

from src.models.music import Genre, SubGenre, GenreName

GENRES = [
    Genre(
        name=GenreName.ROCK,
        description="Rock music is a broad genre of popular music that originated as 'rock and roll' in the United States in the late 1940s and early 1950s, developing into a range of different styles in the mid-1960s and later, particularly in the United Kingdom and the United States."
    ), 
    Genre(
        name=GenreName.POP,
        description="Pop music is a genre of popular music that originated in its modern form during the mid-1950s in the United States and the United Kingdom."
    ), 
    Genre(
        name=GenreName.FUNKSOUL,
        description="Funk is a music genre that originated in African American communities in the mid-1960s when musicians created a rhythmic, danceable new form of music through a mixture of soul, jazz, and R&B. Soul music is a popular music genre that originated in the African American community throughout the United States in the 1950s and early 1960s."
    ),
    Genre(
        name=GenreName.HIPHOP,
        description="Rap is a vocal style, usually coming together with hip-hop, the musical genre off-shoot of the hip hop culture."
    ),
    Genre(
        name=GenreName.JAZZ,
        description="Jazz is a music genre that originated in the African-American communities of New Orleans, United States, in the late 19th and early 20th centuries, with its roots in blues and ragtime."
    ),
    Genre(
        name=GenreName.CLASSICAL,
        description="Classical music is art music produced or rooted in the traditions of Western culture, generally considered to have begun in Europe after the fall of the Western Roman Empire in the late 5th century and continuing to present day."
    ),
    Genre(
        name=GenreName.ELECTRONIC,
        description="Electronic music is music that employs electronic musical instruments, digital instruments, or circuitry-based music technology in its creation.",
        weight=4,
    ),
    Genre(
        name=GenreName.REGGAE,
        description="Reggae is a music genre that originated in Jamaica in the late 1960s."
    ),
    Genre(
        name=GenreName.HOUSE,
        description="House music is a genre of electronic dance music characterized by a repetitive four-on-the-floor beat and a tempo of 120 to 130 beats per minute.",
        weight=4,
    ), 
    Genre(
        name=GenreName.TECHNO,
        description="Techno is a genre of electronic dance music that is characterized by a repetitive beat which is generally produced for use in a continuous DJ set."
    ),
    Genre(
        name=GenreName.DISCO,
        description="Disco is a genre of dance music and a subculture that emerged in the 1970s from the United States' urban nightlife scene."
    ),
    Genre(
        name=GenreName.WORLD,
        description="World music is a musical category encompassing many different styles of music from around the world, including traditional music, neotraditional music, and music where more than one cultural tradition intermingle."
    ),
    Genre(
        name=GenreName.ANY, 
        description="Free track! No genre restrictions on this one.",
    )
]

GENRE_DICT = {genre.name: genre for genre in GENRES}

SUBGENRES = [

    SubGenre(
        name="Classic Rock",
        genre=GENRE_DICT[GenreName.ROCK],
        description="Classic rock is a radio format which developed from the album-oriented rock (AOR) format in the early 1980s."
    ),
    SubGenre(
        name="Psychedelic Rock",
        genre=GENRE_DICT[GenreName.ROCK],
        description="Psychedelic rock is a diverse style of rock music inspired, influenced, or representative of psychedelic culture, which is centred on perception-altering hallucinogenic drugs."
    ),
    SubGenre(
        name="Hard Rock",
        genre=GENRE_DICT[GenreName.ROCK],
        description="Hard rock is a loosely defined subgenre of rock music that began in the mid-1960s, with the garage, psychedelic and blues rock movements."
    ),


    SubGenre(
        name="Pop Rock",
        genre=GENRE_DICT[GenreName.POP],
        description="Pop rock is rock music with a greater emphasis on professional songwriting and recording craft, and less emphasis on attitude."
    ),
    SubGenre(
        name="Synthpop",
        genre=GENRE_DICT[GenreName.POP],
        description="Synth-pop (short for synthesizer pop; also called techno-pop) is a subgenre of new wave music that first became prominent in the late 1970s and features the synthesizer as the dominant musical instrument."
    ),


    SubGenre(
        name="Gangsta Rap",
        genre=GENRE_DICT[GenreName.HIPHOP],
        description="Gangsta rap or gangster rap is a style of hip hop characterized by themes and lyrics that generally emphasize the 'gangsta' lifestyle."
    ),
    SubGenre(
        name="Conscious Rap",
        genre=GENRE_DICT[GenreName.HIPHOP],
        description="Conscious hip hop or socially conscious hip-hop is a subgenre of hip hop that challenges the dominant cultural, political, philosophical, and economic consensus."
    ),
    SubGenre(
        name="Trap",
        genre=GENRE_DICT[GenreName.HIPHOP],
        description="Trap is a subgenre of hip hop music that originated in the Southern United States during the early 1990s. Characterized by its ominous lyrics and sound that incorporate 808 kick drums, triple hi-hats, layered synthesizers, and 'cinematic' strings."
    ),

    

    SubGenre(
        name="Jazz Fusion",
        genre=GENRE_DICT[GenreName.JAZZ],
        description="Jazz fusion (also known as fusion) is a music genre that developed in the late 1960s when musicians combined jazz harmony and improvisation with rock music, funk, and rhythm and blues."
    ),
    SubGenre(
        name="Smooth Jazz",
        genre=GENRE_DICT[GenreName.JAZZ],
        description="Smooth jazz is a genre of commercially oriented crossover jazz that became dominant in the 1980s and early 1990s."
    ),


    SubGenre(
        name="Orchestral",
        genre=GENRE_DICT[GenreName.CLASSICAL],
        description="Orchestral music is a broad category that includes music produced by one or more orchestras, large or small, in Western music."
    ),
    SubGenre(
        name="Symphonic",
        genre=GENRE_DICT[GenreName.CLASSICAL],
        description="Symphonic music is a genre of classical music that comprises the symphony, the concerto, and various forms of orchestral music."
    ),
    SubGenre(
        name="Opera",
        genre=GENRE_DICT[GenreName.CLASSICAL],
        description="Opera is a form of theatre in which music has a leading role and the parts are taken by singers, but is distinct from musical theatre."
    ),
    SubGenre(
        name="Solo Instrument",
        genre=GENRE_DICT[GenreName.CLASSICAL],
        description="Solo instrumental music is a genre of music that features a single instrument playing a piece of music. This can include piano, guitar, violin, cello, and many others."
    ),


    SubGenre(
        name="Ambient",
        genre=GENRE_DICT[GenreName.ELECTRONIC],
        description="Ambient music is a genre of music that emphasizes tone and atmosphere over traditional musical structure or rhythm."
    ),
    SubGenre(
        name="Drum and Bass",
        genre=GENRE_DICT[GenreName.ELECTRONIC],
        description="Drum and bass (also written as 'drum 'n' bass'; commonly abbreviated as 'D&B', 'DnB' or 'D'n'B') is a genre of electronic music characterized by fast breakbeats (typically 160–180 beats per minute) with heavy bass and sub-bass lines, sampled sources, and synthesizers."
    ),
    SubGenre(
        name="UK Garage",
        genre=GENRE_DICT[GenreName.ELECTRONIC],
        description="UK garage (also known as UKG) is a genre of electronic music originating from England in the early 1990s. Characterized by its syncopated 4/4 percussive rhythms."
    ), 
    SubGenre(
        name="Trip Hop",
        genre=GENRES[5],
        description="Trip hop is a musical genre that originated in the early 1990s in the United Kingdom, especially Bristol. Characterized by a 'dirty' sound, downtempo beats, and soulful vocals."
    ),


    SubGenre(
        name="Dub",
        genre=GENRE_DICT[GenreName.REGGAE],
        description="Dub is a genre of electronic music that grew out of reggae in the late 1960s and early 1970s, and is commonly considered a subgenre, though it has developed to extend beyond the scope of reggae."
    ),
    SubGenre(
        name="Reggae",
        genre=GENRE_DICT[GenreName.REGGAE],
        description="Reggae is a music genre that originated in Jamaica in the late 1960s."
    ),


    SubGenre(
        name="Deep House",
        genre=GENRE_DICT[GenreName.HOUSE],
        description="Deep house is a subgenre of house music that originated in the 1980s, initially fusing elements of Chicago house with 1980s jazz-funk and touches of soul music."
    ),
    SubGenre(
        name="Tech House",
        genre=GENRE_DICT[GenreName.HOUSE],
        description="Tech house is a subgenre of house music that combines stylistic features of techno with house."
    ), 
    SubGenre(
        name="Electro House",
        genre= GENRE_DICT[GenreName.HOUSE],
        description="Electro house is a genre of electronic dance music characterized by heavy bass and a tempo around 130 beats per minute."
    ),
    SubGenre(
        name="Future House",
        genre=GENRE_DICT[GenreName.HOUSE],
        description="Future house is a house music genre that emerged in the 2010s, described as a fusion between deep house, UK garage, and incorporating other elements."
    ),
    SubGenre(
        name="Amapiano",
        genre=GENRE_DICT[GenreName.HOUSE],
        description="Amapiano is a style of house music that emerged in South Africa in 2012. Amapiano is a hybrid of deep house, jazz, and lounge music characterized by synths, airy pads, and wide basslines."
    ),
    SubGenre(
        name="French House",
        genre=GENRE_DICT[GenreName.HOUSE],
        description="A late 1990s house sound developed in France. Inspired by the '70s and '80s funk and disco sounds. Mostly features a typical sound 'filter' effect and lower bpm."
    ),
    SubGenre(
        name="Acid House",
        genre=GENRE_DICT[GenreName.HOUSE],
        description="Acid house is a subgenre of house music developed around the mid-1980s by DJs from Chicago. Characterized by the 'squelching' sounds of the Roland TB-303 electronic synthesizer-sequencer."
    ),
    SubGenre(
        name="Tribal House",
        genre=GENRE_DICT[GenreName.HOUSE],
        description="Tribal house is a subgenre of house music which combines traditional house music with world music. Characterized by its heavy use of percussion."
    ),


    SubGenre(
        name="Minimal Techno",
        genre=GENRE_DICT[GenreName.TECHNO],
        description="Minimal techno is a subgenre of techno music. Characterized by a stripped-down aesthetic that exploits the use of repetition and understated development."
    ),
    SubGenre(
        name="Detroit Techno",
        genre=GENRE_DICT[GenreName.TECHNO],
        description="Detroit techno is a type of techno music that generally includes the first techno productions by Detroit-based artists during the 1980s and early 1990s."
    ),
    SubGenre(
        name="Industrial Techno",
        genre=GENRE_DICT[GenreName.TECHNO],
        description="Industrial techno is a subgenre of techno music that originated in the 1990s. Characterized by its dark and aggressive sound, it is influenced by industrial music."
    ), 


    SubGenre(
        name="Italo Disco",
        genre=GENRE_DICT[GenreName.DISCO],
        description="Italo disco is a music genre which originated in Italy and was mainly produced from the late 1970s to the late 1980s. Characterized by a heavy reliance on synthesizers and drum machines."
    ),
    SubGenre(
        name="Nu-Disco",
        genre=GENRE_DICT[GenreName.DISCO],
        description="Nu-disco, also called disco house, is a genre of dance music. Characterized by a fusion of disco and modern electronic dance music."
    ),
    SubGenre(
        name="Disco Funk",
        genre=GENRE_DICT[GenreName.DISCO],
        description="Disco funk is a subgenre of funk music which emerged in the late 1960s and early 1970s. Characterized by its strong bassline and rhythm."
    ), 



    SubGenre(
        name="Bossanova",
        genre=GENRE_DICT[GenreName.WORLD],
        description="Bossa nova is a style of Brazilian music, which was developed and popularized in the 1950s and 1960s and is today one of the best-known Brazilian music styles abroad.",
    ),
    SubGenre(
        name="K-Pop",
        genre=GENRE_DICT[GenreName.WORLD],
        description="K-pop is a genre of popular music originating in South Korea.",
    ),
    SubGenre(
        name="Afrobeat",
        genre=GENRE_DICT[GenreName.WORLD],
        description="Afrobeat is a music genre that involves the combination of elements of West African musical styles such as fuji music and highlife with American funk and jazz influences, with a focus on chanted vocals, complex intersecting rhythms, and percussion.",
    ),
    SubGenre(
        name="Klezmer",
        genre=GENRE_DICT[GenreName.WORLD],
        description="Klezmer is a musical tradition of the Ashkenazi Jews of Eastern Europe. Played by professional musicians called klezmorim, the genre originally consisted largely of dance tunes and instrumental display pieces for weddings and other celebrations.",
    ), 
    SubGenre(
        name="French Variety",
        genre=GENRE_DICT[GenreName.WORLD],
        description="French variety music, also known as chanson française, is a style of music that emerged in France during the 19th and 20th centuries."
    ),
    SubGenre(
        name="Japanese Traditional",
        genre=GENRE_DICT[GenreName.WORLD],
        description="Japanese traditional music is the folk or traditional music of Japan."
    ),
    SubGenre(
        name="Indian Classical",
        genre=GENRE_DICT[GenreName.WORLD],
        description="Indian classical music is the classical music of the Indian subcontinent."
    ),
    SubGenre(
        name="Irish Folk",
        genre=GENRE_DICT[GenreName.WORLD],
        description="Irish traditional music is a genre of folk music that developed in Ireland."
    ),
    SubGenre(
        name="Latin",
        genre=GENRE_DICT[GenreName.WORLD],
        description="Latin music is a genre used by the music industry as a catch-all term for music that comes from Spanish- and Portuguese-speaking areas of the world."
    ),
    SubGenre(
        name="Japanese City Pop",
        genre=GENRE_DICT[GenreName.WORLD],
        description="City pop is a music genre that originated in Japan in the late 1970s. It was originally termed as an offshoot of Japan's Western-influenced 'new music', but came to include a wide range of styles and genres, often characterized by its smooth and romantic sound."
    ),
    SubGenre(
        name="Arabic Pop",
        genre=GENRE_DICT[GenreName.WORLD],
        description="Arabic pop music or Arab pop is a subgenre of pop music and Arabic music."
    )
]