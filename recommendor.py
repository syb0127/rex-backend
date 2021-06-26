import googleapi

def get_recommended_restaurants(lat,lon):
    search_result = googleapi.get_nearby_restaurants(lat,lon)
    return search_result

def adjust_personal_restaurant_rating(place_id, personal_rating):
    #return boolean
    #return false if dbquery fails or if personal_rating is invalid
    rating = dbquery.()
    if (rating is None):
        rating = 5
    calculate the updated_rating
    send the (user_id, place_id, updated rating) to the db

    return True