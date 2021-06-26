import googlemaps
from datetime import datetime
import os

ENVVAR_GOOGLE_API_KEY = "GOOGLE_API_KEY"

gmaps = googlemaps.Client(key=os.environ[ENVVAR_GOOGLE_API_KEY])

def get_nearby_restaurants(lat, lon):
    result = gmaps.places_nearby(location=(lat,lon),radius=300,type="restaurant")
    return result['results']
    