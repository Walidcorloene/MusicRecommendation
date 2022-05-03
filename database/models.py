from datetime import datetime
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class Artistes(db.Model):

    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    __tablename__ = "artistes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    # Auto generated timestamps for creation & update of the row
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Artiste : {self.id} with name : {self.name} >"


@dataclass
class Concerts(db.Model):
    id: int
    
    id_artiste: str
    date_debut: datetime
    date_fin: datetime
    spectacle: str
    festival: str
    salle: str
    lieu: str
    prix: float

    __tablename__ = "concerts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    id_artiste = db.Column(db.Integer, db.ForeignKey(
        'artistes.id'), nullable=False)
    date_debut = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    spectacle = db.Column(db.String(), nullable=False)
    festival = db.Column(db.String())
    salle = db.Column(db.String(), nullable=False)
    lieu = db.Column(db.String(), nullable=False)
    prix = db.Column(db.Float(), nullable=True)

    # Auto generated timestamps for creation & update of the row
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, id_artiste, date_debut, date_fin, spectacle, festival, salle, lieu, prix):
        self.id_artiste = id_artiste
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.spectacle = spectacle
        self.festival = festival
        self.salle = salle
        self.lieu = lieu
        self.prix = prix

    def __repr__(self):
        return f"<le concert {self.id} a été fais par : {self.id_artiste} >"
