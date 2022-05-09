from flask import *
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
from api.apiModel import db_getUserInfo, db_memberSignin, db_checkIfEmailExist, db_addNewMember


userAPI = Blueprint("user api", __name__)

@userAPI.route("/api/user", methods=["GET"])
def checkUserStatus():
    if "name" in session:
        data = db_getUserInfo(session['name'])
        print(data)
        print(session['name'])
        if data:
            return data
        return {"data": None}
    return {"data": None}


@userAPI.route("/api/user", methods=["POST"])
def signup():
    req = request.get_json()
    isExist = db_checkIfEmailExist(req['email'])
    print(isExist)
    if isExist:
        return {
                "error": True,
                "message":"信箱已經被註冊"
        }      
    else:
        db_addNewMember(req['name'], req['email'], req['password'])
        return {"ok":True}

@userAPI.route("/api/user", methods=["PATCH"])
def signin():
    req = request.get_json()
    member = db_memberSignin(req['email'], req['password'])
    if member:
        session['name'] = member[1]
        return {"ok":True}
    else:
        return {"error": True, "message": "信箱或密碼錯誤"}
    

@userAPI.route("/api/user", methods=["DELETE"])
def signout():
    session.pop('name', None)
    return {"ok":True}