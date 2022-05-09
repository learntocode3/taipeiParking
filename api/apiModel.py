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
def db_getUserInfo(name):
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor()
    query = ("SELECT * FROM member WHERE member.name = %s")
    data_query=(name,)
    cursor.execute(query, data_query)
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    data = {}
    data['data'] = {}
    if user:
        data['data']['id'] = user[0]
        data['data']['name'] = user[1]
        data['data']['email'] = user[2]
        return data

#使用者登入
def db_memberSignin(email, password):
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
def db_checkIfEmailExist(email):
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
def db_addNewMember(name, email, password):
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