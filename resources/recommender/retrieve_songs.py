import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import json
import re


# authorization.json contient le client_id et le client_secret nécessaires pour 
# l'authentification auprès de l'API spotify

credentials = json.load(open('resources/recommender/authorization.json')) # endroit où sont stockés mes tokens d'api spotify
client_id = credentials['client_id'] 
client_secret = credentials['client_secret']

# Autorization pour la connexion en cours
scope = 'user-library-read'

client_credentials_manager = SpotifyOAuth(client_id=client_id,client_secret=client_secret, redirect_uri = "http://localhost:8888/callback", scope=scope)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def features_from_url (url, limit):
    if "playlist" in url:
        # On cherche la playlist sur spotify
        tracks = sp.playlist(url, "tracks") 
        tracklist = []

        # On parcourt la réponse de l'API spotify à la recherche de musiques
        for i in tracks["tracks"]["items"]: 
            tracklist.append(i["track"]["uri"])
            #On arrête de chercher des musiques si la limite est atteinte
            if len(tracklist) >= limit: break 
        
    if "track" in url:
        tracklist = re.findall(r'track/([0-9a-zA-Z]*)', url)

    features = sp.audio_features(tracklist)

    # Retourne un DataFrame à partir des features audio récupérées sur spotify, on drop les colonnes qui ne nous intéressent pas
    return pd.DataFrame.from_dict(features).drop(["type", "id", "track_href", "analysis_url", "time_signature"], axis=1)


