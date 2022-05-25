import requests
import sys
sys.path.append('./')
from settings import GOOGLE_API

API = GOOGLE_API
address = '成功路四段61巷8弄3號'

def getGPS(address):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {
        'key': API,
        'address':address
        }
    response = requests.get(base_url, params=params)
    geometry = response.json()['results'][0]['geometry']
    longtitude, latitude = geometry['location']['lng'] , geometry['location']['lat']
    return [latitude, longtitude]

# print('經度 : ', longtitude)
# print('緯度 : ', latitude)

from geopy import distance
# origin = (25.0817187, 121.5930352)
# destination = (25.0803634, 121.5674973)
# print(distance.distance(origin, destination).miles) 1 mile = 1.609 km
# print(distance.distance(origin, destination).km)

def getDistance(lat1,long1,lat2,long2):
    return distance.distance((lat1, long1), (lat2, long2)).km
# d = getDistance(25.0817187, 121.5930352,25.0803634, 121.5674973)
# print(d)

def reverseGeo(latitude, longtitude):
    url= f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longtitude}&language=zh-TW&key={API}"
    response = requests.get(url)
    return response.json()


# 用GOOGLE API 計算經緯度間的距離
# a="https://maps.googleapis.com/maps/api/distancematrix/json?"
# p={
#     'key': API,
#     'origins':'25.0817187,121.5930352',
#     'destinations':'25.0803634,121.5674973'
# }
# response = requests.get(a, params=p)
# print(response.json())