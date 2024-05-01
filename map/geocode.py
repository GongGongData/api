import googlemaps

from gonggongapp.settings import GOOGLE_API_KEY


def get_geocode(address):
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    geocode_result = gmaps.geocode(address, region="kr", language="ko")
    if geocode_result and len(geocode_result) > 0:
        location = geocode_result[0].get("geometry", {}).get("location", {})
        if location:
            lat = location.get("lat")
            lng = location.get("lng")
            return lat, lng
    return None, None
