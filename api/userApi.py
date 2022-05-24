from flask import *
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
import api.apiModel as sql
import requests
import sys
sys.path.append('./')
from settings import PARTNER_KEY



userAPI = Blueprint("user api", __name__)

@userAPI.route("/api/user", methods=["GET"])
def checkUserStatus():
    if "name" in session:
        data = sql.getUserInfo(session['name'])
        print(data)
        # print(data)
        # print(session['name'])
        #--------------------------------------------
        # checkIfOrder = sql.checkOrder(data[0])
        # print(checkIfOrder)
        # if checkIfOrder:
        #     id=checkIfOrder[0]
        # else:
        #     id=None

        
        #     return redirect(f'http://127.0.0.1:3000/order/{id}')
        #-----------------------------------------------------------------
        if data:
            print(data[0])
            return {"data": "ok", 'memberId':data[0]} #, "orderid":id}
        # return {"data": None}
    return {"data": None}


@userAPI.route("/api/user", methods=["POST"])
def signup():
    req = request.get_json()
    isExist = sql.checkIfEmailExist(req['email'])
    # print(isExist)
    if isExist:
        return {
                "error": True,
                "message":"信箱已經被註冊"
        }      
    else:
        memberId = sql.addNewMember(req['name'], req['email'], req['phone'], req['password'])
        return {"memberId":memberId}

@userAPI.route("/api/user", methods=["PATCH"])
def signin():
    req = request.get_json()
    member = sql.memberSignin(req['email'], req['password'])
    if member:
        session['name'] = member[1]
        return {"ok":True}
    else:
        return {"error": True, "message": "信箱或密碼錯誤"}
    

@userAPI.route("/api/user", methods=["DELETE"])
def signout():
    session.pop('name', None)
    return {"ok":True}



@userAPI.route("/api/user/card", methods=["POST"])
def getCreditCard():
    req = request.get_json()
    # print("###########################", req)
    prime=req['prime']
    member_id = req['id']
    personalInfoForCard=sql.getMemberData(member_id)
    print(personalInfoForCard)
    phone_number=personalInfoForCard[4]
    name=personalInfoForCard[1]
    email=personalInfoForCard[2]
    
    #後端發prime/partner_key...等資料給tappay來綁定信用卡取得 card token & key
    tappay_url = 'https://sandbox.tappaysdk.com/tpc/card/bind'
    prime = {
        "prime": prime,
        "partner_key": PARTNER_KEY,
        "merchant_id": "leontien2008_ESUN",
        "currency": "TWD",
        "cardholder": {
            "phone_number": phone_number,
            "name": name,
            "email": email,
        }
    }
    header = {
        'Content-Type': 'application/json',
        'x-api-key': PARTNER_KEY
    }       
    
    body = json.dumps(prime)

    req = requests.post(tappay_url, data=body, headers=header)
    res = req.json()
    print(res)
    card_token = res['card_secret']['card_token']
    card_key = res['card_secret']['card_key']

    sql.addCreditCard(member_id, card_token, card_key)

    return {'data':'ok'}
