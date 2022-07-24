import requests
import sys
sys.path.append('./')
from settings import GOOGLE_API

API = GOOGLE_API

def getGPS(address):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {
        'key': API,
        'address':address
        }
    response = requests.get(base_url, params=params)
    status = response.json()['status']
    print("google api status : ",status)
    if status != "OK":
        return bool(0)
    geometry = response.json()['results'][0]['geometry']
    longtitude, latitude = geometry['location']['lng'] , geometry['location']['lat']
    return [latitude, longtitude]

from geopy import distance

def getDistance(lat1,long1,lat2,long2):
    return distance.distance((lat1, long1), (lat2, long2)).km


def reverseGeo(latitude, longtitude):
    url= f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longtitude}&language=zh-TW&key={API}"
    response = requests.get(url)
    return response.json()

