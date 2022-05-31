from flask import Blueprint
from flask import *
import json
import api.apiModel as sql
# from api.apiModel import db_getIdBySessionName, db_insertToSupply, db_insertToSupplyStatus, db_insertToSupplyTimetable, db_checkIfSpaceNumberExist
from api.gps import getGPS

import sys
sys.path.append('./')
from settings import AWS_KEY_ID, AWS_SECRET_KEY

import boto3

s3 = boto3.client('s3',
                   aws_access_key_id=AWS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_KEY
                )

BUCKET_NAME='aws-test-for-term3'

offerAPI = Blueprint('offer api', __name__)

@offerAPI.route("/api/offer", methods=['POST'])
def insertOffer():

    supplyData=request.form['supplyData']
    req = json.loads(supplyData)
    print(type(supplyData), supplyData)

    image= request.files['iptFile']
    pictureName = image.filename
    print(image, type(image))
    print(pictureName)
    parking_space_image = f'https://d1omjlgso6gyhl.cloudfront.net/{pictureName}'

    # print(session['name'])
    space_onwer_id = sql.getIdBySessionName(session['name'])[0]
    # print(space_onwer_id)
    parking_space_name = req['addressName']
    parking_space_address = req['address']
    parking_space_number = req['parking_space_number']
    # print(parking_space_name, parking_space_address, parking_space_number)
    GPS = getGPS(parking_space_address)
    longtitude = GPS[1]
    latitude = GPS[0]
    # print(longtitude, latitude)
    price_per_hour = req['price']
    # print(price_per_hour)
    time_1_start = req['time']['section-1-start']
    time_1_end = req['time']['section-1-end']
    time_2_start = req['time']['section-2-start']
    time_2_end = req['time']['section-2-end']
    time_3_start = req['time']['section-3-start']
    time_3_end = req['time']['section-3-end']

    #確認有沒有在小表格裡面
    isExist = sql.checkIfSpaceNumberExist(parking_space_address, parking_space_number)
    if isExist:
        return {"data": "車位號碼已經存在"}

    #上傳到s3
    # s3.upload_file(picturePath, BUCKET_NAME, pictureName)
    s3.upload_fileobj(image, BUCKET_NAME, pictureName)
    print('success saved the image to S3')    
    
    #新增資料到四個表
    id = sql.insertToSupply(space_onwer_id, parking_space_name, parking_space_address, parking_space_number, longtitude, latitude, price_per_hour, parking_space_image)
    # print(id)
    sql.insertToCheckSpaceNum(id[0], parking_space_address, parking_space_number)
    sql.insertToSupplyStatus(id[0], "true")
    sql.insertToSupplyTimetable(id[0], time_1_start, time_1_end, time_2_start, time_2_end, time_3_start, time_3_end)
    return {'data':'ok'}


@offerAPI.route("/update/offer", methods=['POST'])
def updateOffer():
    req=request.get_json()
    print(req)
    spaceId=req['spaceId']
    newPrice=req['price']
    newStart1=req['time']['section-1-start']
    newEnd1=req['time']['section-1-end']
    newStart2=req['time']['section-2-start']
    newEnd2=req['time']['section-2-end']
    newStart3=req['time']['section-3-start']
    newEnd3=req['time']['section-3-end']
    if newPrice != "":
        sql.updateSupplyPrice(spaceId, newPrice)
    sql.updateSupplyTime(spaceId, newStart1, newEnd1, newStart2, newEnd2, newStart3, newEnd3)
    return {'data':'ok'}

@offerAPI.route("/get/supply", methods=['GET'])
def getSupply():
    space_onwer_id = sql.getIdBySessionName(session['name'])[0]
    supplyList = sql.getSupplyList(space_onwer_id)
    print('這位會員所提供的所有車位：',supplyList)
    return {'data':supplyList}