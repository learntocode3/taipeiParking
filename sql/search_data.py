import mysql.connector
from mysql.connector import errorcode
import json

import sys
sys.path.append('./')
from settings import USER, PASSWORD


# print(USER,PASSWORD)

# connect to mysql
DB_NAME = 'ezpark'
cnx = mysql.connector.connect(
                                host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com',
                                user=USER,
                                password=PASSWORD,
                                auth_plugin='mysql_native_password')
cursor = cnx.cursor()

#---------------------------------------------------------------------------

#本機端資料庫


# import mysql.connector
# from mysql.connector import errorcode
# import json
# import sys
# sys.path.append('./')
# from settings import USER, PASSWORD

# # print(USER,PASSWORD)

# # connect to mysql
# DB_NAME = 'ezpark'
# cnx = mysql.connector.connect(user=USER,
#                               password=PASSWORD,
#                               auth_plugin='mysql_native_password')
# cursor = cnx.cursor()





cursor.execute("USE {}".format(DB_NAME))


#建立提供者

TABLES = {}
TABLES['search_data'] = (
    "CREATE TABLE `search_data` ("
    "  `user_id` INT NOT NULL,"
    "  `demandAddress` VARCHAR(255) NOT NULL,"
    "  `demandPrice` INT NOT NULL,"
    "  `demandStart` VARCHAR(255) NOT NULL,"
    "  `demandEnd` VARCHAR(255) NOT NULL,"
    "  `search_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  FOREIGN KEY (`user_id`) REFERENCES member (`id`)"
    ") ENGINE=InnoDB")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")