import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Recommander:


    def __init__(self, client_id: str, client_secret: str):

        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )

        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        

    def get_recommandation(self, track_links: list[str], limit: int = 5):

        track_ids = [link.split('/')[-1] for link in track_links]
        recos = self.sp.recommendations(seed_tracks=track_ids, limit=limit)

        reco_links = []
        for reco in recos['tracks']:
            reco_links.append(reco['external_urls']['spotify'])

        return reco_links[:limit]
            
            