import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
from api.gps import getGPS, getDistance
import sys
sys.path.append('./')
from settings import USER, PASSWORD

# dbconfig = { 
#     'host':'ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com',
#     'user':USER,
#     'database':'ezpark',
#     'password':PASSWORD,
#     'auth_plugin':'mysql_native_password'
# }

# cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
#                                                       pool_size = 32,
#                                                       **dbconfig)


    # cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    # cursor = cnx.cursor()


#每次檢查要資料
def getUserInfo(name):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT * FROM member WHERE member.name = %s")
    data_query=(name,)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    return user
    # data = {}
    # data['data'] = {}
    # if user:
    #     data['data']['id'] = user[0]
    #     data['data']['name'] = user[1]
    #     data['data']['email'] = user[2]
    #     return data

def checkOrder(member_id, offset):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT user_order.*, supply.parking_space_address from user_order Left join supply on user_order.parking_space_id=supply.parking_space_id WHERE member_id =%s ORDER BY order_id DESC limit 12 offset %s")
    data_query=(member_id, offset)
    cursor.execute(query, data_query)
    order = cursor.fetchall()
    cursor.close()
    cnx.close()
    return order

#使用者登入
def memberSignin(email, password):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()    
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT * FROM member WHERE member.email = %s AND member.password = %s")
    data_query=(email, password)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    if user:
        #print(user)
        return user

#檢查使用者信箱是否已經被註冊
def checkIfEmailExist(email):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT * FROM member WHERE member.email = %s")
    data_query=(email, )
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    return bool(user)
  

#使用者註冊
def addNewMember(name, email, phone, password):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    add_member = ("INSERT INTO member "
                  "(name, email, password, phone) " 
                  "VALUES (%s, %s, %s, %s)")
    data_member = (name, email, password, phone)
    cursor.execute(add_member, data_member)
    cnx.commit()
    print("成功新增使用者")
    cursor.execute("SELECT LAST_INSERT_ID();")
    id = cursor.fetchone()
    cursor.close()
    cnx.close()
    print("成功取得 member ID")
    return id[0]

def getMemberData(member_id):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()    
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT * FROM member WHERE id = %s")
    data_query=(member_id, )
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    return user
  
# a = getMemberData(9)
# print(a)

def addCreditCard(member_id, card_token, card_key):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()

    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    change_status = ("UPDATE member SET card_token=%s, card_key=%s WHERE id= %s")
    card_data = (card_token, card_key, member_id)
    cursor.execute(change_status, card_data)
    cnx.commit()
    print("新增card")
    cursor.close()
    cnx.close()  


#通過session name 得到 member ID
def getIdBySessionName(name):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()    
    
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT member.id FROM member WHERE member.name = %s")
    data_query=(name,)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    if user:
        return user    

#新增資料到supply
def insertToSupply(space_onwer_id, parking_space_name, parking_space_address,parking_space_number, longtitude, latitude,price_per_hour, parking_space_image):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()    
    
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    add_supply = ("INSERT INTO supply "
                  "(space_onwer_id, parking_space_name, parking_space_address,parking_space_number, longtitude, latitude,price_per_hour, parking_space_image) " 
                  "VALUES (%s, %s, %s,%s, %s, %s, %s, %s)")
    data_supply = (space_onwer_id, parking_space_name, parking_space_address,parking_space_number, longtitude, latitude,price_per_hour, parking_space_image)
    cursor.execute(add_supply, data_supply)
    cnx.commit()
    print("supply新增成功")
    cursor.execute("SELECT LAST_INSERT_ID();")
    id = cursor.fetchone()
    cursor.close()
    cnx.close()
    print("成功取得新增ID")
    return id

def insertToSupplyStatus(parking_space_id, space_status):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()    
    
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    add_supply_status = ("INSERT INTO supply_status "
                  "VALUES (%s, %s)")
    data_supply = (parking_space_id, space_status)
    cursor.execute(add_supply_status, data_supply)
    cnx.commit()
    print("supply status 新增成功")
    cursor.close()
    cnx.close()


def insertToSupplyTimetable(id, time_1_start, time_1_end, time_2_start, time_2_end, time_3_start, time_3_end):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()    
    
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    add_supply_timetable = ("INSERT INTO supply_timetable "
                  "VALUES (%s, %s, %s,%s, %s, %s, %s)")
    data_supply = (id, time_1_start, time_1_end, time_2_start, time_2_end, time_3_start, time_3_end)
    cursor.execute(add_supply_timetable, data_supply)
    cnx.commit()
    print("supply timetable 新增成功")
    cursor.close()
    cnx.close()


def checkIfSpaceNumberExist(parking_space_address, parking_space_number):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()

    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT * FROM check_spaceNum WHERE parking_space_address = %s AND parking_space_number= %s")
    data_query=(parking_space_address, parking_space_number)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    return bool(user)

def selectAllGps():
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()

    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT supply.latitude, supply.longtitude, supply.parking_space_id FROM supply JOIN supply_status ON supply.parking_space_id = supply_status.parking_space_id WHERE supply_status.space_status='true' ")
    cursor.execute(query,)
    allGPS = cursor.fetchall()
    cursor.close()
    cnx.close()
    return allGPS

# a = selectAllGps()
# print(a)

def checkTime(parkingID):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()

    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT * FROM supply_timetable WHERE parking_space_id = %s")
    data_query=(parkingID, )
    cursor.execute(query, data_query)
    timetable = cursor.fetchone()
    cursor.close()
    cnx.close()
    return timetable

# a = checkTime(4)
# print(a)

def getAddressNumPriceById(parkingID):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT parking_space_address, price_per_hour, parking_space_number, parking_space_image FROM supply WHERE parking_space_id = %s")
    data_query=(parkingID, )
    cursor.execute(query, data_query)
    info = cursor.fetchone()
    cursor.close()
    cnx.close()
    return info

# a = getAddressPriceById(7)
# print(a)
def getComment(parkingID):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("select feedback.comment, feedback.star, user_order.parking_space_id from feedback left join user_order on feedback.order_id = user_order.order_id where parking_space_id = %s")
    data_query=(parkingID, )
    cursor.execute(query, data_query)
    comment = cursor.fetchall()
    cursor.close()
    cnx.close()
    print(comment)
    return comment

def insertToCheckSpaceNum(parking_space_id, parking_space_address, parking_space_number):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    add_supply_checkSpaceNum = ("INSERT INTO check_spaceNum "
                  "VALUES (%s, %s, %s)")
    data_supply = (parking_space_id, parking_space_address, parking_space_number)
    cursor.execute(add_supply_checkSpaceNum, data_supply)
    cnx.commit()
    print("supply checkSpaceNum 新增成功")
    cursor.close()
    cnx.close()    


def insertUserSearch(user_id, demandAddress, demandPrice, demandStart, demandEnd):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    add_searchData = ("INSERT INTO search_data (user_id, demandAddress, demandPrice, demandStart, demandEnd)"
                  "VALUES (%s, %s, %s, %s, %s)")
    data_supply = (user_id, demandAddress, demandPrice, demandStart, demandEnd)
    cursor.execute(add_searchData, data_supply)
    cnx.commit()
    print("add_searchData 新增成功")
    cursor.close()
    cnx.close()   


# insertUserSearch(1, "asdfasd", 21, "12:30", "15:30")

def getSearchData(user_id):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT * FROM search_data WHERE user_id = %s ORDER BY search_time DESC LIMIT 0,1")
    data_query=(user_id,)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    return user

# a = getSearchData(1)
# print(a)


def insertOrder(user_id, spaceId, current_time, final_price):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    add_order = ("INSERT INTO user_order (member_id, parking_space_id, time_start, final_price)"
                  "VALUES (%s, %s, %s, %s)")
    data_order = (user_id, spaceId, current_time, final_price)
    cursor.execute(add_order, data_order)
    cnx.commit()
    print("order 新增成功")
    cursor.execute("SELECT LAST_INSERT_ID();")
    id = cursor.fetchone()
    cursor.close()
    cnx.close()
    print("成功新增的訂單ID")
    return id

# a = insertOrder(2, 8, "13:00")
# print(a)

def changeSpaceStatusToFalse(spaceId):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    change_status = ("UPDATE supply_status SET space_status='false' WHERE parking_space_id= %s")
    id = (spaceId,)
    cursor.execute(change_status, id)
    cnx.commit()
    print("車位狀況變更為false")
    cursor.close()
    cnx.close()

# changeSpaceStatusToFalse(4)


def changeSpaceStatusToTrue(spaceId):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    change_status = ("UPDATE supply_status SET space_status='true' WHERE parking_space_id= %s")
    id = (spaceId,)
    cursor.execute(change_status, id)
    cnx.commit()
    print("車位狀況變更為true")
    cursor.close()
    cnx.close()       

# changeSpaceStatusToTrue(5)
# changeSpaceStatusToTrue(7)
# changeSpaceStatusToTrue(9)
# changeSpaceStatusToTrue(10)


def updateOrder(order_id, finish_time):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    change_status = ("UPDATE user_order SET time_end=%s WHERE order_id= %s")
    finish_time = (finish_time, order_id)
    cursor.execute(change_status, finish_time)
    cnx.commit()
    print("新增結束時間")
    cursor.close()
    cnx.close()  


def getOrderData(orderId):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT * FROM user_order WHERE order_id = %s ")
    data_query=(orderId,)
    cursor.execute(query, data_query)
    data = cursor.fetchone()
    cursor.close()
    cnx.close()
    return data

# a = getOrderData(4)
# print(a)

def getCardSecret(user_id):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT card_token, card_key FROM member WHERE id = %s")
    data_query=(user_id,)
    cursor.execute(query, data_query)
    data = cursor.fetchone()
    cursor.close()
    cnx.close()
    return data

# a = getCardSecret(11)
# print(a)

def addRecTradeId(orderId, rec_trade_id, totalFee):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    change_status = ("UPDATE user_order SET rec_trade_id=%s, total_fee=%s WHERE order_id= %s")
    rec_trade_data = (rec_trade_id, totalFee, orderId)
    cursor.execute(change_status, rec_trade_data)
    cnx.commit()
    print("新增 rec_trade_id 成功")
    cursor.close()
    cnx.close()  

# addRecTradeId(16, 'D20220517YrljSY')


def getrecTradeId(orderId):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    query = ("SELECT rec_trade_id FROM user_order WHERE order_id = %s")
    data_query=(orderId,)
    cursor.execute(query, data_query)
    data = cursor.fetchone()
    cursor.close()
    cnx.close()
    return data

# a = getrecTradeId(16)
# print(a[0])

# 用 1 小時內所有的搜尊資料來計算熱門程度
def getPop(supplyAddress):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("select * from search_data where search_time > now() - interval 1 hour")
    cursor.execute(query,)
    searchDataWithin1Hour = cursor.fetchall()
    cursor.close()
    cnx.close()
    print("所有的搜尋紀錄：", searchDataWithin1Hour)
    if searchDataWithin1Hour:
    
        # 計算（已經篩選完可以提供的車位）跟 （一小時以內被搜尋的地址們）的距離 

        toleranceDistance = 1 # 1km 為可接受的距離
        popularity = 0
        for i in range(len(searchDataWithin1Hour)):
            # print(searchDataWithin1Hour)
            # print("###################",i,"############",searchDataWithin1Hour[i][1])
            demand = getGPS(searchDataWithin1Hour[i][1])
            if demand == False:
                continue 
            supply = getGPS(supplyAddress)
            if supply == False:
                continue
            dist = getDistance(supply[0], supply[1], demand[0], demand[1])

            if dist <= toleranceDistance:
                popularity += 1
        print("###Popularity: ", popularity)        
        return popularity
    print("###Popularity: ", 0) 
    return 0

# a = getPop('基隆路一段380巷14號')
# print(a)


def getSupplyList(space_onwer_id):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("select * from supply where space_onwer_id= %s ")
    data_query=(space_onwer_id,)
    cursor.execute(query, data_query)
    data = cursor.fetchall()
    cursor.close()
    cnx.close()
    return data

def updateSupplyPrice(spaceId, newPrice):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    # cnx = cnxpool.get_connection()
    # cursor = cnx.cursor()
    change_status = ("UPDATE supply SET price_per_hour=%s WHERE parking_space_id= %s")
    price_data = (newPrice, spaceId)
    cursor.execute(change_status, price_data)
    cnx.commit()
    print("更改價錢成功")
    cursor.close()
    cnx.close()  

def updateSupplyTime(spaceId, newStart1, newEnd1, newStart2, newEnd2, newStart3, newEnd3):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    change_status = ("UPDATE supply_timetable SET time_1_start = %s, time_1_end = %s, time_2_start = %s, time_2_end = %s, time_3_start = %s, time_3_end = %s WHERE parking_space_id= %s")
    time_data = (newStart1, newEnd1, newStart2, newEnd2, newStart3, newEnd3, spaceId)
    cursor.execute(change_status, time_data)
    cnx.commit()
    print("更改時間成功")
    cursor.close()
    cnx.close()  



def insertToFeedBack(order_id, comment, star):
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    add_comment = ("INSERT INTO feedback (order_id, comment, star) "
                  "VALUES (%s, %s, %s)")
    data_comment = (order_id, comment, star)
    cursor.execute(add_comment, data_comment)
    cnx.commit()
    print("feedback 新增成功")
    cursor.close()
    cnx.close()    



def getAvailable():
    cnx = mysql.connector.connect(host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com', user=USER, password=PASSWORD, database='ezpark', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("select supply.parking_space_address, supply_status.space_status from supply inner join supply_status on supply.parking_space_id = supply_status.parking_space_id where supply_status.space_status = 'true'")
    cursor.execute(query,)
    allAvailable = cursor.fetchall()
    cursor.close()
    cnx.close()
    return allAvailable