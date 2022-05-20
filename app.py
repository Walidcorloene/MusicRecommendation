from flask import Flask
from flask import jsonify
from flask_restful import Api
from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
# from flask_migrate import Migrate
# from database.models import db
# from resources.artists import ArtistsApi, ArtistConcertsApi

from resources.recommendations import RecommendationAPI

import os


app = Flask(__name__, instance_relative_config=True)

# Loads configuration from config.py
app.config.from_object('config')


## Initialisation des modules
# db.init_app(app)
#custom_cli(app)
# migrate = Migrate(app, db)
#setup_open_food_fact(app)
api = Api(app)
Bcrypt(app)
# JWTManager(app)


api.add_resource(RecommendationAPI, '/recommendations')


print(os.environ.get("TICKETMASTER_APIKEY"))



@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World from Food Buy API"})

if __name__ == "__main__":
    app.run(debug=True, port=3000)