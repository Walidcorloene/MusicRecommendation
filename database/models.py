from datetime import datetime
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class Artistes(db.Model):

    id: int
    nom: str
    created_at: datetime
    updated_at: datetime

    __tablename__ = "artistes"
    id = db.column(db.Interger, primary_key=True, autoincrement=True)
    name = db.column(db.String(), nullable=False, unique=True)
    # Auto generated timestamps for creation & update of the row
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Artiste : {self.id} with name : {self.name} >"


@dataclass
class concerts(db.Model):
    id_concert: int
    artiste: str
    date_debut: datetime
    date_fin: datetime
    spectacle: str
    festival: str
    salle: str
    lieu: str
    prix: float

    __tablename__ = "concerts"
    id_concert = db.column(db.Interger, primary_key=True, autoincrement=True)
    id_artiste = db.column(db.Interger, db.ForeignKey(
        'artistes.id'), nullable=False)
    date_debut = db.column(db.DateTime)
    date_fin = db.column(db.DateTime)
    spectacle = db.column(db.String(), nullable=False)
    festival = db.column(db.String())
    salle = db.column(db.String(), nullable=False)
    lieu = db.column(db.String(), nullable=False)
    prix = db.column(db.Float(), nullable=False)

    # Auto generated timestamps for creation & update of the row
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, id_concert, id_artiste, date_debut, date_fin, spectacle, festival, salle, lieu, prix):
        self.id_concert = id_concert
        self.id_artiste = id_artiste
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.spectacle = spectacle
        self.festival = festival
        self.salle = salle
        self.lieu = lieu
        self.prix = prix

    def __repr__(self):
        return f"<le concert {self.id_concert} a été fais par : {self.id_artiste} >"
