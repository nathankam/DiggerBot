

from src.models.music import Genre, SubGenre

GENRES = [
    Genre(
        name="Rock",
        description="Rock music is a broad genre of popular music that originated as 'rock and roll' in the United States in the late 1940s and early 1950s, developing into a range of different styles in the mid-1960s and later, particularly in the United Kingdom and the United States."
    ), 
    Genre(
        name="Pop",
        description="Pop music is a genre of popular music that originated in its modern form during the mid-1950s in the United States and the United Kingdom."
    ), 
    Genre(
        name="Rap",
        description="Rap is a vocal style, usually coming together with hip-hop, the musical genre off-shoot of the hip hop culture."
    ),
    Genre(
        name="Jazz",
        description="Jazz is a music genre that originated in the African-American communities of New Orleans, United States, in the late 19th and early 20th centuries, with its roots in blues and ragtime."
    ),
    Genre(
        name="Classical",
        description="Classical music is art music produced or rooted in the traditions of Western culture, generally considered to have begun in Europe after the fall of the Western Roman Empire in the late 5th century and continuing to present day."
    ),
    Genre(
        name="Electronic",
        description="Electronic music is music that employs electronic musical instruments, digital instruments, or circuitry-based music technology in its creation.",
        weight=4,
    ),
    Genre(
        name="Reggae",
        description="Reggae is a music genre that originated in Jamaica in the late 1960s."
    ),
    Genre(
        name="House",
        description="House music is a genre of electronic dance music characterized by a repetitive four-on-the-floor beat and a tempo of 120 to 130 beats per minute.",
        weight=4,
    ), 
    Genre(
        name="Techno",
        description="Techno is a genre of electronic dance music that is characterized by a repetitive beat which is generally produced for use in a continuous DJ set."
    ),
    Genre(
        name="Disco",
        description="Disco is a genre of dance music and a subculture that emerged in the 1970s from the United States' urban nightlife scene."
    ),
    Genre(
        name="Folk",
        description="Folk music includes traditional folk music and the genre that evolved from it during the 20th-century folk revival."
    ), 
    Genre(
        name="Free Track", 
        description="Free track! No genre restrictions on this one! Go wild :)"
    )
]


SUBGENRES = [
    SubGenre(
        name="Classic Rock",
        genre=GENRES[0],
        description="Classic rock is a radio format which developed from the album-oriented rock (AOR) format in the early 1980s."
    ),
    SubGenre(
        name="Psychedelic Rock",
        genre=GENRES[0],
        description="Psychedelic rock is a diverse style of rock music inspired, influenced, or representative of psychedelic culture, which is centred on perception-altering hallucinogenic drugs."
    ),
    SubGenre(
        name="Pop Rock",
        genre=GENRES[1],
        description="Pop rock is rock music with a greater emphasis on professional songwriting and recording craft, and less emphasis on attitude."
    ),
    SubGenre(
        name="Dance Pop",
        genre=GENRES[1],
        description="Dance-pop is a pop and dance subgenre that originated in the early 1980s."
    ),
    SubGenre(
        name="Synthpop",
        genre=GENRES[1],
        description="Synth-pop (short for synthesizer pop; also called techno-pop) is a subgenre of new wave music that first became prominent in the late 1970s and features the synthesizer as the dominant musical instrument."
    ),
    SubGenre(
        name="Gangsta Rap",
        genre=GENRES[2],
        description="Gangsta rap or gangster rap is a style of hip hop characterized by themes and lyrics that generally emphasize the 'gangsta' lifestyle."
    ),
    SubGenre(
        name="Conscious Rap",
        genre=GENRES[2],
        description="Conscious hip hop or socially conscious hip-hop is a subgenre of hip hop that challenges the dominant cultural, political, philosophical, and economic consensus."
    ),
    SubGenre(
        name="Jazz Fusion",
        genre=GENRES[3],
        description="Jazz fusion (also known as fusion) is a music genre that developed in the late 1960s when musicians combined jazz harmony and improvisation with rock music, funk, and rhythm and blues."
    ),
    SubGenre(
        name="Smooth Jazz",
        genre=GENRES[3],
        description="Smooth jazz is a genre of commercially oriented crossover jazz that became dominant in the 1980s and early 1990s."
    ),
    SubGenre(
        name="Orchestral",
        genre=GENRES[4],
        description="Orchestral music is a broad category that includes music produced by one or more orchestras, large or small, in Western music."
    ),
    SubGenre(
        name="Symphonic",
        genre=GENRES[4],
        description="Symphonic music is a genre of classical music that comprises the symphony, the concerto, and various forms of orchestral music."
    ),
    SubGenre(
        name="Ambient",
        genre=GENRES[5],
        description="Ambient music is a genre of music that emphasizes tone and atmosphere over traditional musical structure or rhythm."
    ),
    SubGenre(
        name="Drum and Bass",
        genre=GENRES[5],
        description="Drum and bass (also written as 'drum 'n' bass'; commonly abbreviated as 'D&B', 'DnB' or 'D'n'B') is a genre of electronic music characterized by fast breakbeats (typically 160–180 beats per minute) with heavy bass and sub-bass lines, sampled sources, and synthesizers."
    ),
    SubGenre(
        name="UK Garage",
        genre=GENRES[5],
        description="UK garage (also known as UKG) is a genre of electronic music originating from England in the early 1990s. Characterized by its syncopated 4/4 percussive rhythms."
    ), 
    SubGenre(
        name="Trip Hop",
        genre=GENRES[5],
        description="Trip hop is a musical genre that originated in the early 1990s in the United Kingdom, especially Bristol. Characterized by a 'dirty' sound, downtempo beats, and soulful vocals."
    ),
    SubGenre(
        name="Dub",
        genre=GENRES[6],
        description="Dub is a genre of electronic music that grew out of reggae in the late 1960s and early 1970s, and is commonly considered a subgenre, though it has developed to extend beyond the scope of reggae."
    ),
    SubGenre(
        name="Reggae",
        genre=GENRES[6],
        description="Reggae is a music genre that originated in Jamaica in the late 1960s."
    ),
    SubGenre(
        name="Deep House",
        genre=GENRES[7],
        description="Deep house is a subgenre of house music that originated in the 1980s, initially fusing elements of Chicago house with 1980s jazz-funk and touches of soul music."
    ),
    SubGenre(
        name="Tech House",
        genre=GENRES[7],
        description="Tech house is a subgenre of house music that combines stylistic features of techno with house."
    ), 
    SubGenre(
        name="Progressive House",
        genre=GENRES[7],
        description="Progressive house is a style (subgenre) of house music that emerged in the early 1990s. Characterized by its 'progressive' nature, it combines elements of house music with other electronic dance music genres."
    ),
    SubGenre(
        name="Electro House",
        genre=GENRES[7],
        description="Electro house is a genre of electronic dance music characterized by heavy bass and a tempo around 130 beats per minute."
    ),
    SubGenre(
        name="Amapiano",
        genre=GENRES[7],
        description="Amapiano is a style of house music that emerged in South Africa in 2012. Amapiano is a hybrid of deep house, jazz, and lounge music characterized by synths, airy pads, and wide basslines."
    ),
    SubGenre(
        name="French House",
        genre=GENRES[7],
        description="A late 1990s house sound developed in France. Inspired by the '70s and '80s funk and disco sounds. Mostly features a typical sound 'filter' effect and lower bpm."
    ),
    SubGenre(
        name="Acid House",
        genre=GENRES[7],
        description="Acid house is a subgenre of house music developed around the mid-1980s by DJs from Chicago. Characterized by the 'squelching' sounds of the Roland TB-303 electronic synthesizer-sequencer."
    ),
    SubGenre(
        name="Ghetto House",
        genre=GENRES[7],
        description="Ghetto house, booty house or G-house is a genre of Chicago house which started being recognized as a distinct style from around 1992 onwards."
    ),
    SubGenre(
        name="Tribal House",
        genre=GENRES[7],
        description="Tribal house is a subgenre of house music which combines traditional house music with world music. Characterized by its heavy use of percussion."
    ),
    SubGenre(
        name="Minimal Techno",
        genre=GENRES[8],
        description="Minimal techno is a subgenre of techno music. Characterized by a stripped-down aesthetic that exploits the use of repetition and understated development."
    ),
    SubGenre(
        name="Detroit Techno",
        genre=GENRES[8],
        description="Detroit techno is a type of techno music that generally includes the first techno productions by Detroit-based artists during the 1980s and early 1990s."
    ),
    SubGenre(
        name="Industrial Techno",
        genre=GENRES[8],
        description="Industrial techno is a subgenre of techno music that originated in the 1990s. Characterized by its dark and aggressive sound, it is influenced by industrial music."
    ), 
    SubGenre(
        name="Italo Disco",
        genre=GENRES[9],
        description="Italo disco is a music genre which originated in Italy and was mainly produced from the late 1970s to the late 1980s. Characterized by a heavy reliance on synthesizers and drum machines."
    ),
    SubGenre(
        name="Nu-Disco",
        genre=GENRES[9],
        description="Nu-disco, also called disco house, is a genre of dance music. Characterized by a fusion of disco and modern electronic dance music."
    )
]