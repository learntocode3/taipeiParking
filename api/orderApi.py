from flask import Blueprint
from flask import *
import json
from api.gps import getGPS, getDistance
import api.apiModel as sql

orderAPI = Blueprint('order api', __name__)

@orderAPI.route("/api/order", methods=['POST'])
def getOrderData():
    req=request.get_json()
    print(req)
    return {'data':"ok"}