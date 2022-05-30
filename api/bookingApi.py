from flask import Blueprint
from flask import *
import json
from api.gps import getGPS, getDistance, reverseGeo
import api.apiModel as sql

bookingAPI = Blueprint('booking api', __name__)

@bookingAPI.route("/api/available", methods=['GET'])
def getAvailable():
    availableData = sql.getAvailable()
    return {'availableData':availableData}

@bookingAPI.route("/api/getUserLocation", methods=['POST'])
def getUserLocation():
    req=request.get_json()
    # print(req)
    address = reverseGeo(req['latitude'], req['longtitude'])
    curAddress = address['results'][0]['formatted_address']
    return {'data':curAddress}

@bookingAPI.route("/api/booking", methods=['POST'])
def insertSearch():
    req=request.get_json()
    # print(req)
    user_id = sql.getIdBySessionName(session['name'])[0]
    demandAddress = req['address']
    demandPrice = req['price']
    demandStart = req['start']
    demandEnd = req['end']
    
    sql.insertUserSearch(user_id, demandAddress, demandPrice, demandStart, demandEnd)
    return {"data":"ok"}
    
@bookingAPI.route("/api/booking", methods=['GET'])           
def getMatchResult():
    user_id = sql.getIdBySessionName(session['name'])[0]

    data = sql.getSearchData(user_id)
    demandAddress = data[1] #req['address']
    demandGps = getGPS(demandAddress)
    demandPrice = data[2] #req['price']
    demandStart = data[3] #req['start']
    demandEnd = data[4] #req['end']


    #列出所有可以列出的資料
    supplyGPS = sql.selectAllGps()

    #計算查詢座標之間的所有距離
    toleranceDistance = 1 # 1km 為可接受的距離
    availableParkingInfo = [] # （車位id，幾點到幾點， 地址， 幾號車位，收費，留言，評分，圖片連結） 
    for i in range(len(supplyGPS)):
        # print(allGPS[i][0],allGPS[i][1])
        

        dist = getDistance(supplyGPS[i][0], supplyGPS[i][1], demandGps[0], demandGps[1])
        if dist <= toleranceDistance:
            parkingID = supplyGPS[i][2]
            supplyTime = sql.checkTime(parkingID)
            supplyStart1 = supplyTime[1]
            supplyEnd1 = supplyTime[2] 
            supplyStart2 = supplyTime[3] 
            supplyEnd2 = supplyTime[4] 
            supplyStart3 = supplyTime[5] 
            supplyEnd3 = supplyTime[6]  
            
            if (supplyStart1 <= demandStart) and (demandEnd <= supplyEnd1):
                supplyAddressNamePrice = sql.getAddressNumPriceById(parkingID)
                supplyAddress = supplyAddressNamePrice[0]
                supplyPrice = supplyAddressNamePrice[1]
                supplySpaceNumber = supplyAddressNamePrice[2]
                supplySpaceImage = supplyAddressNamePrice[3]
                supplyFinalPrice = getAdjustPrice(supplyAddress, int(supplyPrice))
                comment = sql.getComment(parkingID)
                message = [ ele[0] for ele in comment ]
                stars = [ ele[1] for ele in comment ]
                supplyInfo = (parkingID, supplyStart1, supplyEnd1, supplyAddress, supplySpaceNumber ,supplyFinalPrice, dist, message, stars, supplySpaceImage)
                availableParkingInfo.append(supplyInfo)
            
            if (supplyStart2 == "") and (supplyEnd2 == ""):
                pass
            else:
                if (supplyStart2 <= demandStart) and (demandEnd <= supplyEnd2):
                    supplyAddressNamePrice = sql.getAddressNumPriceById(parkingID)
                    supplyAddress = supplyAddressNamePrice[0]
                    supplyPrice = supplyAddressNamePrice[1]
                    supplySpaceNumber = supplyAddressNamePrice[2]
                    supplySpaceImage = supplyAddressNamePrice[3]
                    supplyFinalPrice = getAdjustPrice(supplyAddress, int(supplyPrice))
                    comment = sql.getComment(parkingID)
                    message = [ ele[0] for ele in comment ]
                    stars = [ ele[1] for ele in comment ]
                    supplyInfo = (parkingID, supplyStart2, supplyEnd2, supplyAddress, supplySpaceNumber ,supplyFinalPrice, dist, message, stars, supplySpaceImage)
                    availableParkingInfo.append(supplyInfo)
            
            if (supplyStart3 == "") and (supplyEnd3 == ""):
                pass
            else:
                if (supplyStart3 <= demandStart) and (demandEnd <= supplyEnd3):
                    supplyAddressNamePrice = sql.getAddressNumPriceById(parkingID)
                    supplyAddress = supplyAddressNamePrice[0]
                    supplyPrice = supplyAddressNamePrice[1]
                    supplySpaceNumber = supplyAddressNamePrice[2]
                    supplySpaceImage = supplyAddressNamePrice[3]
                    supplyFinalPrice = getAdjustPrice(supplyAddress, int(supplyPrice))
                    comment = sql.getComment(parkingID)
                    message = [ ele[0] for ele in comment ]
                    stars = [ ele[1] for ele in comment ]
                    supplyInfo = (parkingID, supplyStart3, supplyEnd3, supplyAddress, supplySpaceNumber ,supplyFinalPrice, dist, message, stars, supplySpaceImage)
                    availableParkingInfo.append(supplyInfo)
    
    print( "所有符合篩選條件的車位：", availableParkingInfo)
    return {"data":availableParkingInfo}

#imporove efficiectcy #寫一個reset supplyDict function

supplyDict = {} 

def getAdjustPrice(supplyAddress, base_price):
    if supplyAddress in supplyDict:
        print(supplyDict)
        popularity = supplyDict[supplyAddress]
    else:
        popularity = sql.getPop(supplyAddress)
        supplyDict[supplyAddress] = popularity
    # print("###",popularity)
    supplyPrice = computePrice(base_price, popularity)
    return  supplyPrice

def computePrice(base_price, popularity):
    supplyPrice = base_price * (1 + (popularity/100)*3)
    print("### 拿到popularity後經過運算得到的價錢：",supplyPrice)
    return supplyPrice


# a = getAdjustPrice("基隆路一段380巷14號", 70)
# print(a)

#low
 
#high

# his = [(2,56),(6,57)]

# sort 33 67

# low = ? 
# high = ? 