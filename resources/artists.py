from flask import jsonify
from flask_restful import Resource
from database.models import Artistes, db, User

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

class ArtistApi(Resource):
    def get(self, artistId):
        # filters the artist and get the first item with next
        existing_artist = Artistes.query.filter(Artistes.id == artistId).first()
        if existing_artist == None:
            return {'error': 'Artistes with id %s not found' % artistId}, 404
        return jsonify(existing_artist)

    def delete(self, artistId):
        try:
            existing_artist = Artistes.query.filter_by(id=artistId).first()
            if existing_artist == None:
                return {'error': 'Artistes with id %s not found' % artistId}, 404
            db.session.delete(existing_artist)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'error': 'Couldnt delete user because : %s' % e}, 400
        return {'message': 'Artistes with id %s was deleted' % artistId}, 200
