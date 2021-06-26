import googleapi
#import something from './dbquery.py'

def get_recommended_restaurants(lat,lon):
    search_result = googleapi.get_nearby_restaurants(lat,lon)
    cleaned_search_result = cleanup_results(search_result)
    return cleaned_search_result

def cleanup_results(search_result):
    return [format_restaurant_entry(r) for r in search_result]

def format_restaurant_entry(restaurant):
    return {'name': restaurant['name'], 'opening hours': restaurant['opening hours'], 'photos': restaurant['photos'], 'rating': restaurant['rating'], 'vicinity': restaurant['vicinity'], 'types': restaurant['types']} 