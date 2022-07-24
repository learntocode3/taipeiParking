import mysql.connector
from mysql.connector import errorcode
import json

import sys
sys.path.append('./')
from settings import USER, PASSWORD

# connect to mysql
DB_NAME = 'ezpark'
cnx = mysql.connector.connect(
                                host='ezpark-space.cfplaoqwsox0.us-east-1.rds.amazonaws.com',
                                user=USER,
                                password=PASSWORD,
                                auth_plugin='mysql_native_password')
cursor = cnx.cursor()

cursor.execute("USE {}".format(DB_NAME))

TABLES = {}
TABLES['feedback'] = (
    "CREATE TABLE `feedback` ("
    "  `order_id` INT,"
    "  `feedback_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  `comment` VARCHAR(255) NOT NULL,"
    "  `star` VARCHAR(255) NOT NULL,"
    "  FOREIGN KEY (`order_id`) REFERENCES user_order (`order_id`)"
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

cursor.close()
cnx.close()