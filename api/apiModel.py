import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling
import sys
sys.path.append('./')
from settings import USER, PASSWORD

dbconfig = {
    
    'user':USER,
    'database':'ezpark',
    'password':PASSWORD,
    'auth_plugin':'mysql_native_password'
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                                                      pool_size = 32,
                                                      **dbconfig)


#每次檢查要資料
def getUserInfo(name):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM member WHERE member.name = %s")
    data_query=(name,)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    return bool(user)
    # data = {}
    # data['data'] = {}
    # if user:
    #     data['data']['id'] = user[0]
    #     data['data']['name'] = user[1]
    #     data['data']['email'] = user[2]
    #     return data

#使用者登入
def memberSignin(email, password):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
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
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM member WHERE member.email = %s")
    data_query=(email, )
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    return bool(user)
  

#使用者註冊
def addNewMember(name, email, password):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    add_member = ("INSERT INTO member "
                  "(name, email, password) " 
                  "VALUES (%s, %s, %s)")
    data_member = (name, email, password)
    cursor.execute(add_member, data_member)
    cnx.commit()
    print("成功新增使用者")
    cursor.close()
    cnx.close()

#通過session name 得到 member ID
def getIdBySessionName(name):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT member.id FROM member WHERE member.name = %s")
    data_query=(name,)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    if user:
        return user    

#新增資料到supply
def insertToSupply(space_onwer_id, parking_space_name, parking_space_address,parking_space_number, longtitude, latitude,price_per_hour):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    add_supply = ("INSERT INTO supply "
                  "(space_onwer_id, parking_space_name, parking_space_address,parking_space_number, longtitude, latitude,price_per_hour) " 
                  "VALUES (%s, %s, %s,%s, %s, %s, %s)")
    data_supply = (space_onwer_id, parking_space_name, parking_space_address,parking_space_number, longtitude, latitude,price_per_hour)
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
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    add_supply_status = ("INSERT INTO supply_status "
                  "VALUES (%s, %s)")
    data_supply = (parking_space_id, space_status)
    cursor.execute(add_supply_status, data_supply)
    cnx.commit()
    print("supply status 新增成功")
    cursor.close()
    cnx.close()


def insertToSupplyTimetable(id, time_1_start, time_1_end, time_2_start, time_2_end, time_3_start, time_3_end):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    add_supply_timetable = ("INSERT INTO supply_timetable "
                  "VALUES (%s, %s, %s,%s, %s, %s, %s)")
    data_supply = (id, time_1_start, time_1_end, time_2_start, time_2_end, time_3_start, time_3_end)
    cursor.execute(add_supply_timetable, data_supply)
    cnx.commit()
    print("supply timetable 新增成功")
    cursor.close()
    cnx.close()


def checkIfSpaceNumberExist(parking_space_address, parking_space_number):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM check_spaceNum WHERE parking_space_address = %s AND parking_space_number= %s")
    data_query=(parking_space_address, parking_space_number)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    return bool(user)

def selectAllGps():
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT latitude, longtitude, parking_space_id FROM supply ")
    cursor.execute(query,)
    allGPS = cursor.fetchall()
    cursor.close()
    cnx.close()
    return allGPS