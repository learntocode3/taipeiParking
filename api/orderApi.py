from flask import Blueprint
from flask import *
import json
from api.gps import getGPS, getDistance
import api.apiModel as sql
from datetime import datetime


orderAPI = Blueprint('order api', __name__)

@orderAPI.route("/api/start/order", methods=['POST'])
def getOrderData():
    #取得前端訂單資訊
    req=request.get_json()
    print(req)
    user_id = sql.getIdBySessionName(session['name'])[0]
    spaceId=req['spaceId']

    #將車位變更為使用中
    sql.changeSpaceStatusToFalse(spaceId)
    
    #輸入使用者開始使用時間並取得訂單編號
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    # print(current_time)
    order_id = sql.insertOrder(user_id, spaceId, current_time)
    return {'orderId':order_id[0],
            'spaceId':spaceId,
            'startTime':current_time,
            'status':"ok"
    }

@orderAPI.route("/api/finish/order", methods=['POST'])
def finishOrder():
    req=request.get_json()
    # print(req)
    orderId=req['orderId']
    orderData = sql.getOrderData(orderId)
    user_id = orderData[1] 
    spaceId=orderData[2]
    startTime=orderData[3]
    print(startTime)

    # #車位恢復提供並新增結束時間到訂單
    sql.changeSpaceStatusToTrue(spaceId)
    now = datetime.now()
    finish_time = now.strftime("%H:%M")
    print(finish_time)
    sql.updateOrder(orderId, finish_time)

    #計算本次停車時數
    startTime = datetime.strptime(startTime,'%H:%M')
    finish_time = datetime.strptime(finish_time,'%H:%M')

    UsageMinutes =  finish_time - startTime
    UsageMinutes = UsageMinutes.total_seconds()/60.0

    print(UsageMinutes, type(UsageMinutes))






    return {'data':"ok"}