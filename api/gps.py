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
    return [longtitude, latitude]

# print('經度 : ', longtitude)
# print('緯度 : ', latitude)