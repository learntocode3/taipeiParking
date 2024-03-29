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

#---------------------------------------------------------------------------
cursor.execute("USE {}".format(DB_NAME))
TABLES = {}
TABLES['member'] = (
    "CREATE TABLE `member` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `name` VARCHAR(255) NOT NULL,"
    "  `email` VARCHAR(255) NOT NULL,"
    "  `password` VARCHAR(255) NOT NULL,"
    "  `phone` VARCHAR(255) NOT NULL,"
    "  `card_token` VARCHAR(255),"
    "  `card_key` VARCHAR(255),"
    "  PRIMARY KEY (`id`)"
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