from flask import Blueprint
from flask import *
import json
from api.gps import getGPS, getDistance
import api.apiModel as sql

bookingAPI = Blueprint('booking api', __name__)

@bookingAPI.route("/api/booking", methods=['POST'])
def insertSearch():
    req=request.get_json()
    print(req)
    address = req['address']
    gps = getGPS(address)
    price = req['price']
    start = req['start']
    end = req['end']
    
    #列出所有可以列出的資料
    allGPS = sql.selectAllGps()
    #計算查詢座標之間的所有距離







    return {'data':'ok'}

