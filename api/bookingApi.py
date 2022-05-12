from flask import Blueprint
from flask import *
import json
from api.gps import getGPS, getDistance
import api.apiModel as sql

bookingAPI = Blueprint('booking api', __name__)

@bookingAPI.route("/api/booking", methods=['POST'])
def insertSearch():
    req=request.get_json()
    # print(req)
    demandAddress = req['address']
    demandGps = getGPS(demandAddress)
    demandPrice = req['price']
    demandStart = req['start']
    demandEnd = req['end']
    
    #列出所有可以列出的資料
    supplyGPS = sql.selectAllGps()

    #計算查詢座標之間的所有距離
    toleranceDistance = 1 # 1km 為可接受的距離
    availableParkingInfo = [] # （車位id，幾點到幾點， 地址， 幾號車位，收費） 
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
                supplyInfo = (parkingID, supplyStart1, supplyEnd1, supplyAddress, supplySpaceNumber ,supplyPrice)
                availableParkingInfo.append(supplyInfo)
            
            if (supplyStart2 == "") and (supplyEnd2 == ""):
                pass
            else:
                if (supplyStart2 <= demandStart) and (demandEnd <= supplyEnd2):
                    supplyAddressNamePrice = sql.getAddressNumPriceById(parkingID)
                    supplyAddress = supplyAddressNamePrice[0]
                    supplyPrice = supplyAddressNamePrice[1]
                    supplySpaceNumber = supplyAddressNamePrice[2]
                    supplyInfo = (parkingID, supplyStart2, supplyEnd2, supplyAddress, supplySpaceNumber ,supplyPrice)
                    availableParkingInfo.append(supplyInfo)
            
            if (supplyStart3 == "") and (supplyEnd3 == ""):
                pass
            else:
                if (supplyStart3 <= demandStart) and (demandEnd <= supplyEnd3):
                    supplyAddressNamePrice = sql.getAddressNumPriceById(parkingID)
                    supplyAddress = supplyAddressNamePrice[0]
                    supplyPrice = supplyAddressNamePrice[1]
                    supplySpaceNumber = supplyAddressNamePrice[2]
                    supplyInfo = (parkingID, supplyStart3, supplyEnd3, supplyAddress, supplySpaceNumber ,supplyPrice)
                    availableParkingInfo.append(supplyInfo)
    
    print( "測試", availableParkingInfo)
    return {"data":availableParkingInfo}
    
            













