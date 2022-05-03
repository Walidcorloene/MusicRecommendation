from flask import jsonify
from flask_restful import Resource
from database.models import Artistes, Concerts, db
from .scraper.artist import Artist

# /artist routes

class ArtistsApi(Resource):
    def get(self):
        # The jsonify module will transforms python
        # dict to JSON objects (not needed for strings, numbers)
        artist = Artistes.query.all()
        return jsonify(artist)

    def delete(self):
        try:
            num_rows_deleted = db.session.query(Artistes).delete()
            db.session.commit()
            return {'message': '%d artist were deleted' % num_rows_deleted}, 200
        except:
            db.session.rollback()
            return {'error': 'Couldnt delete all artist'}, 422


# /artist/<artistId> routes

class ArtistConcertsApi(Resource):
    def get(self, artistName):
        # filters the artist and get the first item with next
        existing_artist = Artistes.query.filter(Artistes.name == artistName).first()
        
        if not existing_artist:    
            artist_to_add = Artistes(name=artistName)
            db.session.add(artist_to_add)
            db.session.commit()
            
            concerts = Artist(artistName, headless=False).concerts
            
            id_artiste = Artistes.query.filter(Artistes.name == artistName).first().id
            for concert in concerts:
                concert_to_add = Concerts(
                    id_artiste=id_artiste,
                    date_debut=concert["date_debut"],
                    date_fin=concert["date_fin"],
                    spectacle=concert["spectacle"],
                    festival=concert["festival"],
                    salle=concert["salle"],
                    lieu=concert["lieu"],
                    prix=concert["prix"]
                )
                db.session.add(concert_to_add)
                db.session.commit()
        else:
            concerts = Concerts.query.filter(Concerts.id_artiste == existing_artist.id).all()
                
        return jsonify(concerts)

    def delete(self, artistName):
        try:
            existing_artist = Artistes.query.filter_by(id=artistName).first()
            if existing_artist == None:
                return {'error': 'Artistes with id %s not found' % artistId}, 404
                
        except Exception as e:
            print(e)
            return {'error': 'Couldnt delete user because : %s' % e}, 400
        return {'message': 'Artistes with id %s was deleted' % artistId}, 200
