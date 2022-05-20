import pandas as pd

import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from .retrieve_songs import features_from_url

import joblib

df_features = pd.read_pickle("resources/recommender/song_features_df.pkl")

# On récupère uniquement l'uri des musiques
df_features["track_uri"] = df_features["track_uri"].apply(lambda x: x.split(":")[2])

# Dataframe contenant les données numériques à normaliser
df_num = df_features[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']]

# On récupère le scaler pour les features des musiques
scaler = joblib.load("resources/recommender/scaler.save")

# On normalise les données qui vont nous servir à faire la recommandation
df_num_scaled = scaler.transform(df_num)

def get_recommended_artists(test):
    """
    Prend un dataframe de features audio en entrée et retourne des noms d'artistes recommandés.
    Le dataframe est normalisé à partir du dataset initial, puis on calcule la similarité cosinus 
    entre les lignes du dataframe et le dataset initial.

    On retourne ensuite un set (pour éviter les doublons) des artistes les plus proches de nos entrées.
    """
    
    if test.shape[0] == 1: # Si on recommande à partir d'une seule musique
        print("L'input est une musique seule")
        track_scaled = scaler.transform(test.drop("uri", axis=1))
        track_cos = cosine_similarity(track_scaled, df_num_scaled)
        sim_scores = list(enumerate(track_cos[0]))
        best_recommended = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # On retourne les noms des artistes en cherchant son index dans le dataframe initial
        return set([df_features.loc[i[0]]["track_name"] for i in best_recommended[1:100]])

    else:
        print("L'input est une playlist")
        tracks_scaled = scaler.transform(test.drop("uri", axis=1))
        tracks_cos = cosine_similarity(tracks_scaled, df_num_scaled)

        sim_scores = []
        for row in tracks_cos:
            sim_scores.extend(list(enumerate(row)))
        best_recommended = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # On retourne les noms des artistes en cherchant son index dans le dataframe initial
        return list(set([df_features.loc[i[0]]["artist_name"] for i in best_recommended[1:100]]))
