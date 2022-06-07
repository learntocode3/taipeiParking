from flask import Blueprint
from flask import *
import json
from api.gps import getGPS, getDistance, reverseGeo
import api.apiModel as sql
from datetime import datetime, timedelta


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

    availableParkingInfo = [] # （車位id，幾點到幾點， 地址， 幾號車位，收費，留言，評分，圖片連結） 

    demandAddress = data[1] #req['address']
    demandGps = getGPS(demandAddress)
    if demandGps == False:
        return {"data":availableParkingInfo}
    demandPrice = data[2] #req['price']
    demandStart = data[3] #req['start']
    demandEnd = data[4] #req['end']


    #列出所有可以列出的資料
    supplyGPS = sql.selectAllGps() 

    #計算查詢座標之間的所有距離
    toleranceDistance = 1 # 1km 為可接受的距離

    for i in range(len(supplyGPS)): # O(n)
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
                supplyFinalPrice = getAdjustPrice(supplyAddress, int(supplyPrice), demandAddress)
                comment = sql.getComment(parkingID)
                message = [ ele[0] for ele in comment ]
                stars = [ ele[1] for ele in comment ]
                lastTenOrdersAvg = sql.getTenLastestOrderAveragePrice(parkingID)
                supplyInfo = (parkingID, supplyStart1, supplyEnd1, supplyAddress, supplySpaceNumber ,supplyFinalPrice, dist, message, stars, supplySpaceImage, lastTenOrdersAvg)
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
                    supplyFinalPrice = getAdjustPrice(supplyAddress, int(supplyPrice), demandAddress)
                    comment = sql.getComment(parkingID)
                    message = [ ele[0] for ele in comment ]
                    stars = [ ele[1] for ele in comment ]
                    lastTenOrdersAvg = sql.getTenLastestOrderAveragePrice(parkingID)
                    supplyInfo = (parkingID, supplyStart2, supplyEnd2, supplyAddress, supplySpaceNumber ,supplyFinalPrice, dist, message, stars, supplySpaceImage, lastTenOrdersAvg)
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
                    supplyFinalPrice = getAdjustPrice(supplyAddress, int(supplyPrice), demandAddress)
                    comment = sql.getComment(parkingID)
                    message = [ ele[0] for ele in comment ]
                    stars = [ ele[1] for ele in comment ]
                    lastTenOrdersAvg = sql.getTenLastestOrderAveragePrice(parkingID)
                    supplyInfo = (parkingID, supplyStart3, supplyEnd3, supplyAddress, supplySpaceNumber ,supplyFinalPrice, dist, message, stars, supplySpaceImage, lastTenOrdersAvg)
                    availableParkingInfo.append(supplyInfo)
    
    print( "所有符合篩選條件的車位：", availableParkingInfo)
    return {"data":availableParkingInfo}

#imporove efficiectcy #寫一個reset supplyDict function

# supplyDict = {} 
import redis
default_time = 3600

supplyDict = redis.Redis(decode_responses=True)

def getAdjustPrice(supplyAddress, base_price, demandAddress):
    print('快取字典：', supplyDict.keys())
    if supplyAddress in supplyDict.keys():
        print('有進入到快取')
        # nowTime=datetime.now() - timedelta(hours=8)
        # print("被存入紀錄 popularity 的字典:", supplyDict)
        # popularity = supplyDict[supplyAddress]
        popularity = int(supplyDict.get(supplyAddress)) + 1
        supplyDict.setex(supplyAddress, default_time, popularity)
        #現有的每一筆資料時間是否合理, clean
        # clean = [] # 只保留符合 1 小時內的資料
        # for i in range(len(supplyDict[supplyAddress])): 
        #     timeDif = nowTime - supplyDict[supplyAddress][i][1]
        #     minutes = timeDif.total_seconds() / 60
        #     print('#跟現在的時間差：', minutes, '分鐘')
        #     if minutes < 60:
        #         print('大於60分鐘的資料：', supplyDict[supplyAddress][i])
        #         # del supplyDict[supplyAddress][i]
        #         # i -= 1
        #         clean.append(supplyDict[supplyAddress][i])
        # supplyDict[supplyAddress] = clean
        
        #加入當前資料
        # supplyDict[supplyAddress].append([demandAddress, nowTime])
        # popularity = supplyDict[supplyAddress]
        popularity = int(supplyDict.get(supplyAddress))
    else:
        print('沒有進入到快取')
        popularity = sql.getPop(supplyAddress)
        supplyDict.setex(supplyAddress, default_time, popularity)
    # print("###",popularity)
    # print('拿進去computePrice的pop:',len(popularity))
    print('拿進去computePrice的pop:', popularity)
    # supplyPrice = computePrice(base_price, len(popularity))
    supplyPrice = computePrice(base_price, popularity)
    return  supplyPrice

def computePrice(base_price, popularity):
    supplyPrice = base_price * (1 + (popularity/100)*3)
    print("### 拿到popularity後經過運算得到的價錢：",supplyPrice)
    return supplyPrice


#low
 
#high

# his = [(2,56),(6,57)]

# sort 33 67

# low = ? 
# high = ? 