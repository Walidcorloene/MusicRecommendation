from flask import jsonify, request
from flask_restful import Resource


from .recommender.retrieve_songs import features_from_url
from .recommender.content_based import get_recommended_artists
from .recommender.tm_concerts import get_concerts

# /artist routes

class RecommendationAPI(Resource):
    def get(self):
        try:
            body = request.get_json()
            tracklist = features_from_url(body["elementURL"], body["limit"])
        except Exception as e:
            print("La/les musique(s) n'ont pas pu être retrouvée(s) :", e)

        recomm_artists = get_recommended_artists(tracklist)

        all_concerts = []

        limit = 15 if (len(recomm_artists) > 15) else len(recomm_artists)

        # On prend seulement les X premiers artistes pour des raisons pratiques
        for artist in recomm_artists[:limit]:
            print("Artiste : ", artist)
            all_concerts.extend(get_concerts(artist))
        
        print("Envoi des concerts recommandés")
        return jsonify(sorted(all_concerts, key=lambda x: x["date"]))
