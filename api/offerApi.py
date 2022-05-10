from flask import Blueprint
from flask import *
import json
from api.apiModel import db_getIdBySessionName, db_insertToSupply, db_insertToSupplyStatus, db_insertToSupplyTimetable
from api.gps import getGPS

offerAPI = Blueprint('offer api', __name__)

@offerAPI.route("/api/offer", methods=['POST'])
def insertOffer():
    req=request.get_json()
    print(req)
    # print(session['name'])
    space_onwer_id = db_getIdBySessionName(session['name'])[0]
    # print(space_onwer_id)
    parking_space_name = req['addressName']
    parking_space_address = req['address']
    parking_space_number = req['parking_space_number']
    # print(parking_space_name, parking_space_address, parking_space_number)
    GPS = getGPS(parking_space_address)
    longtitude = GPS[0]
    latitude = GPS[1]
    # print(longtitude, latitude)
    price_per_hour = req['price']
    print(price_per_hour)
    time_1_start = req['time']['section-1-start']
    time_1_end = req['time']['section-1-end']
    time_2_start = req['time']['section-2-start']
    time_2_end = req['time']['section-2-end']
    time_3_start = req['time']['section-3-start']
    time_3_end = req['time']['section-3-end']

    #新增資料到三個表
    id = db_insertToSupply(space_onwer_id, parking_space_name, parking_space_address, parking_space_number, longtitude, latitude, price_per_hour)
    # print(id)
    db_insertToSupplyStatus(id[0], "true")
    db_insertToSupplyTimetable(id[0], time_1_start, time_1_end, time_2_start, time_2_end, time_3_start, time_3_end)

    return {'data':'ok'}