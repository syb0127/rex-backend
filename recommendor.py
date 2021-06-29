import googleapi
import dbquery

def get_recommended_restaurants(lat,lon):
    search_result = googleapi.get_nearby_restaurants(lat,lon)
    return search_result

def adjust_personal_restaurant_rating(user_id, place_id, personal_rating):
    #return boolean
    #return false if dbquery fails or if personal_rating is invalid
    #TODO 6/27/21 
    rating = dbquery.get_rating(user_id, place_id)
    if (rating is None):
        rating = 5
    rating += personal_rating * 0.5
    update = dbquery.update_restaurant_rating(user_id, place_id, rating)
    return update is not None