import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='correcaoExercicios4')

def get_data( data ):
    index, row = data
    time.sleep(3)

    # Chamada API
    response = geolocator.reverse(row['query'])

    address = response.raw['address']

    place_id = response.raw['place_id'] if 'place_id' in response.raw else 'NA'
    osm_type = response.raw['osm_type'] if 'osm_type' in response.raw else 'NA'
    county = address['county'] if 'county' in address else 'NA'
    country_code = address['country_code'] if 'country_code' in address else 'NA'

    return place_id, osm_type, county, country_code

