import googlemaps
from datetime import datetime
import os
from flask import current_app

ENVVAR_GOOGLE_API_KEY = "GOOGLE_API_KEY"

gmaps = googlemaps.Client(key=os.environ[ENVVAR_GOOGLE_API_KEY])

def get_nearby_restaurants(lat, lon):
    result = gmaps.places_nearby(location=(lat,lon),radius=1000,type="restaurant")
    current_app.logger.warning(result)
    return result['results']
    