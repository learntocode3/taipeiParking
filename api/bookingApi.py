from flask import Blueprint
from flask import *
import json

bookingAPI = Blueprint('booking api', __name__)

@bookingAPI.route("/api/booking", methods=['POST'])
def insertSearch():
    req=request.get_json()
    print(req)
    return {'data':'ok'}

