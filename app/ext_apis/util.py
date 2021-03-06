import logging

import math
import requests
import reverse_geocoder as rg
from scipy import spatial


def get_short_url(target_url):
    test_access_token = '20f07f91f3303b2f66ab6f61698d977d69b83d64'
    api_url = 'https://api.pics.ee/v1/links/?access_token={}'.format(test_access_token)
    r = requests.post(api_url, data={"url": target_url})
    if r.status_code == 200:
        return r.json()['data']['picseeUrl']
    else:
        logging.getLogger(__name__).error(r.status_code)


def get_exchange_rate():
    r = requests.get('https://tw.rter.info/capi.php')
    mapping = r.json()
    return mapping


def get_like_eth_liquid():
    r = requests.get('https://api.liquid.com/products')
    result = r.json
    like_eth = result[210]
    name = like_eth['currency_pair_code']
    volume = like_eth["volume_24h"]
    last_price = like_eth["last_price_24h"]
    ts = like_eth["last_event_timestamp"]
    ts = int(float(ts))
    return name, volume, last_price, ts


def get_like_coinmarketcap():
    r = requests.get('https://graphs2.coinmarketcap.com/currencies/likecoin/')
    result = r.json()
    [timestamp_ms, price] = result['price_usd'][-1]
    return timestamp_ms, price


def get_reservoir_stat():
    r = requests.get('https://www.taiwanstat.com/waters/latest')
    return r.json()[0]


def reverse_geocode_customize(coordinates):
    # free database: https://simplemaps.com/resources/free-country-cities
    # local, database, oldest: https://github.com/thampiman/reverse-geocoder
    # forwarding, older: https://github.com/DenisCarriere/geocoder
    # forwarding, newer: https://github.com/alexreisner/geocoder
    """
    :param coordinates: list of tuples,
    e.g. (51.5214588, -0.1729636), (9.936033, 76.259952), (37.38605, -122.08385)
    :return: list of dict, e.g.
    [
      {
        'name': 'Cochin',
        'cc': 'IN',
        'lat': '9.93988',
        'lon': '76.26022',
        'admin1': 'Kerala',
        'admin2': 'Ernakulam'
      },
    ]
    """
    results = rg.search(coordinates)  # default mode = 2
    return results


def cartesian(latitude, longitude, _elevation=0):
    # Convert to radians
    latitude = latitude * (math.pi / 180)
    longitude = longitude * (math.pi / 180)

    R = 6371  # 6378137.0 + elevation  # relative to centre of the earth
    X = R * math.cos(latitude) * math.cos(longitude)
    Y = R * math.cos(latitude) * math.sin(longitude)
    Z = R * math.sin(latitude)
    return X, Y, Z


def build_kd_tree(list_of_coords):
    places = []
    for coordinates in list_of_coords:
        cartesian_coord = cartesian(*coordinates)
        places.append(cartesian_coord)
    tree = spatial.KDTree(places)
    return tree


def gps_dms_to_dd(dms):
    """
    :param dms: list of degrees, minutes, seconds
    :return:
    """
    degrees, minutes, seconds = dms[0], dms[1], dms[2]
    decimal_degrees = degrees + (minutes/60.0) + (seconds/3600.0)
    return decimal_degrees
