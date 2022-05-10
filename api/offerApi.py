from flask import Blueprint
from flask import *
import json

offerAPI = Blueprint('offer api', __name__)

@offerAPI.route("/api/offer", methods=['POST'])
def insertSearch():
    req=request.get_json()
    print(req)
    return {'data':'ok'}