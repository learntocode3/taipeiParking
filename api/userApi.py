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
        print("##########",session['name'])
        data = sql.getUserInfo(session['name'])
        if data:
            print(data[0])
            return {"data": "ok", 'memberId':data[0]} 
    return {"data": None}


@userAPI.route("/api/user", methods=["POST"])
def signup():
    req = request.get_json()
    isExist = sql.checkIfEmailExist(req['email'])
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
    print(member)
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
