import pandas as pd
import requests

from datetime import datetime as dt

import os



API_KEY = os.environ.get("TICKETMASTER_APIKEY")
FIND_ARTIST_URL = "https://app.ticketmaster.com/discovery/v2/attractions.json"
SEARCH_EVENTS_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def get_artist_id(artist) -> str :
    """
    Retourn l'ID d'un artiste en cherchant son nom
    """
    response = requests.get(FIND_ARTIST_URL, params={"apikey":API_KEY, "keyword":artist}).json()
    try: 
        return response["_embedded"]["attractions"][0]["id"]

    except KeyError:
        print(f"L'artiste {artist} n'a pas été trouvé")

def get_concerts(artist) -> list[dict]:
    """
    Retourne une liste des concerts pour l'artiste recherché
    """
    artist_id = get_artist_id(artist)

    response = requests.get(SEARCH_EVENTS_URL, params={
                        "apikey": API_KEY, 
                        "attractionId": artist_id,
                        "locale": "*"}).json()

    concerts_list = []
    try:
        for c in response["_embedded"]["events"]:
            concert = {}

            concert["artist"] = artist
            concert["link"] = c["url"]
            try:
                concert["date"] = dt.combine(
                    dt.strptime(c["dates"]["start"]["localDate"], "%Y-%m-%d"),
                    dt.strptime(c["dates"]["start"]["localTime"], "%H:%M:%S").time()
                )
            except KeyError:
                print(f"Erreur : le temps local n'a pas été retroué pour ce concert -> {concert['link']}")
                concert["date"] = dt.strptime(c["dates"]["start"]["localDate"], "%Y-%m-%d")

            try:
                concert["prix"] = c["priceRanges"][0]["min"]
            except KeyError:
                print(f"Erreur : le prix n'a pas pu être trouvé pour ce concert -> {concert['link']}")
            
            concert["place"] = c["_embedded"]["venues"][0]["name"]
            concert["postalCode"] = c["_embedded"]["venues"][0]["postalCode"]
            concert["city"] = c["_embedded"]["venues"][0]["city"]["name"]
            concert["country"] = c["_embedded"]["venues"][0]["country"]["name"]

            concerts_list.append(concert)
    except KeyError:
        print(f"{artist} n'a aucun concert de prévu")
        
    return concerts_list