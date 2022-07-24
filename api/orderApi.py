from sqlite3 import adapt
from flask import Blueprint
from flask import *
import json
from api.gps import getGPS, getDistance
import api.apiModel as sql
from datetime import datetime
import requests
import sys
sys.path.append('./')
from settings import PARTNER_KEY


orderAPI = Blueprint('order api', __name__)

@orderAPI.route("/get/revenue", methods=['GET'])
def getRevenue():
    space_onwer_id = sql.getIdBySessionName(session['name'])[0]
    revenue = sql.getRevenue(space_onwer_id)
    return {'data':revenue}



@orderAPI.route("/api/allOrder", methods=['GET'])
def getAllOrder():
    orderOffset = request.args.get('orderOffset','0')
    orderOffset = int(orderOffset)
    user_id = sql.getIdBySessionName(session['name'])[0]
    # 設定offset
    offset = 12 * orderOffset
    orderData = sql.checkOrder(user_id, offset)
    print('最新12筆訂單資料：', orderData)
    finished = []
    unfinished = []
    for i in range(len(orderData)):
        if orderData[i][4] == "":
            unfinished.append((orderData[i][0], orderData[i][8], orderData[i][3], orderData[i][4], orderData[i][7]))
        else:
            finished.append((orderData[i][0], orderData[i][8], orderData[i][3], orderData[i][4], orderData[i][7]))
    return {'unfinish':unfinished, 'finish':finished}




@orderAPI.route("/api/feedback", methods=['POST'])
def insertFeedBack():
    req=request.get_json()
    sql.insertToFeedBack(req['orderId'],req['comment'], req['star'])
    return {'data':'ok'}


@orderAPI.route("/api/render/order", methods=['POST'])
def renderOrderData():
    req=request.get_json()
    orderId=req['orderId']
    orderData = sql.getOrderData(orderId)
    startTime=orderData[3]
    finalPricePerHour=orderData[6]
    now = datetime.now()
    upToTime = now.strftime("%H:%M")
    startTime = datetime.strptime(startTime,'%H:%M')
    finish_time = datetime.strptime(upToTime,'%H:%M')
    UsageMinutes =  finish_time - startTime
    UsageMinutes = int(UsageMinutes.total_seconds()/60.0)
    finalPrice = int((UsageMinutes*finalPricePerHour)/60)
    return {'finalPrice':finalPrice}



@orderAPI.route("/api/start/order", methods=['POST'])
def getOrderData():
    #取得前端訂單資訊
    req=request.get_json()
    print(req)
    user_id = sql.getIdBySessionName(session['name'])[0]
    spaceId=req['spaceId']
    finalPrice=req['finalPrice']

    #將車位變更為使用中
    #check if ture for update
    affectedRow = sql.changeSpaceStatusToFalse(spaceId)
    print('######## AFFECTED ROWS #######', affectedRow)
    if affectedRow != 1:
        return {'status':'order failed'}
        
    #輸入使用者開始使用時間並取得訂單編號
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    order_id = sql.insertOrder(user_id, spaceId, current_time, finalPrice)
    return {'orderId':order_id[0],
            'spaceId':spaceId,
            'startTime':current_time,
            'finalPrice':finalPrice,
            'status':"ok"
    }

@orderAPI.route("/api/finish/order", methods=['POST'])
def finishOrder():
    req=request.get_json()
    orderId=req['orderId']
    orderData = sql.getOrderData(orderId)
    print(orderData)
    user_id = orderData[1] 
    spaceId=orderData[2]
    startTime=orderData[3]
    finalPricePerHour=orderData[6]

    # #車位恢復提供並新增結束時間到訂單
    sql.changeSpaceStatusToTrue(spaceId)
    now = datetime.now()
    finish_time = now.strftime("%H:%M")
    sql.updateOrder(orderId, finish_time)

    #計算本次停車時數
    startTime = datetime.strptime(startTime,'%H:%M')
    finish_time = datetime.strptime(finish_time,'%H:%M')

    UsageMinutes =  finish_time - startTime
    UsageMinutes = int(UsageMinutes.total_seconds()/60.0)
    finalPrice = int((UsageMinutes*finalPricePerHour)/60)

    print("本次通車時間為：", UsageMinutes, type(UsageMinutes))
    print("本次每分鐘收費為：", finalPrice, type(UsageMinutes))

    #結帳
    card = sql.getCardSecret(user_id)
    card_token = card[0]
    card_key = card[1]

    tappay_url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-token'
    prime = {
        "card_key": card_key,
        "card_token": card_token,
        "partner_key": PARTNER_KEY,
        "currency": "TWD",
        "merchant_id": "leontien2008_ESUN",
        "details":"TapPay Test",
        "amount": finalPrice + 5
    }
            
    header = {
        'Content-Type': 'application/json',
        'x-api-key': PARTNER_KEY
    }       
        
    body = json.dumps(prime)

    req = requests.post(tappay_url, data=body, headers=header)
    userPayResult = req.json()
    print(userPayResult)

    status=userPayResult['status']
    rec_trade_id=userPayResult['rec_trade_id']
    totalFee=userPayResult['amount']

    sql.addRecTradeId(orderId, rec_trade_id, totalFee)
    if status == 0:
        return {'data':"ok", "orderId":orderId}

    return {'data':"card fail"}



@orderAPI.route("/api/refund/order", methods=['POST'])
def refundOrder():
    req=request.get_json()
    orderId=req['orderId']
    rec_trade_id = sql.getrecTradeId(orderId)

    tappay_url = 'https://sandbox.tappaysdk.com/tpc/transaction/refund'
    prime = {
        "partner_key": PARTNER_KEY,
        "rec_trade_id": rec_trade_id[0]
    }
        
        
    header = {
        'Content-Type': 'application/json',
        'x-api-key': PARTNER_KEY
    }       
        
    body = json.dumps(prime)

    req = requests.post(tappay_url, data=body, headers=header)
    userPayResult = req.json()
    print(userPayResult)

    return {'data':'refundOk'}