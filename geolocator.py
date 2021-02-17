from geopy.geocoders import Nominatim
from geopy import distance


# Accepts a USA city name in the format "montoursville pennsylvania"
# Returns an array of [str(lat), str(lon)]
def point_for_city_state(city_name):
    geo_locator = Nominatim(user_agent="my_user_agent")
    country = "USA"
    loc = geo_locator.geocode(city_name + ',' + country)
    return tuple((loc.latitude, loc.longitude))


# Accepts 2 tuples of points (lat1, lon1) (lat2, lon2)
# Returns the distance between them in miles
def distance_between_points(city1, city2):
    dist = distance.distance(city1, city2).miles
    return dist


# Accepts 2 tuples of point and an int of miles
# Returns true if the distance between two cities is no greater than the int of miles
# Accurate within ~ 30 miles
def is_within_miles(city1, city2, miles):
    dist = distance_between_points(city1, city2)
    return dist <= miles


def test():
    city1 = point_for_city_state("williamsport pennsylvania")
    print(city1)
    city2 = point_for_city_state("scranton pennsylvania")
    print(city2)
    dist = distance_between_points(city1, city2)
    print(is_within_miles(city1, city2, 70))


# test()
