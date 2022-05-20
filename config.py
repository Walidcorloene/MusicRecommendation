import os
from dotenv import load_dotenv

PROPAGATE_EXCEPTIONS = True
# ENVIRONNEMENT CONFIGURATION

## Load .env file
load_dotenv(verbose=True)


## Database config

DEVELOPMENT = True
DEBUG = True
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_DATABASE_URI = os.getenv("postgresql://postgres:whitebeard@localhost:5432/postgres", default="postgresql://postgres:whitebeard@localhost:5432/postgres")
