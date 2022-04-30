from flask import Flask
from flask import jsonify
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from database.models import db
from cli.cli import custom_cli

app = Flask(__name__, instance_relative_config=True)

# Loads configuration from config.py
app.config.from_object('config')
## From here you can access config variables like this:
## value_from_config = app.config['CONFIG_VARIABLE_NAME']

## Initialisation des modules
db.init_app(app)
custom_cli(app)
migrate = Migrate(app, db)
setup_open_food_fact(app)
api = Api(app)
Bcrypt(app)
JWTManager(app)
app.run(debug=True)

## Declaration of API routes




@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World from Food Buy API"})
