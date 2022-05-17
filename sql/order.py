import mysql.connector
from mysql.connector import errorcode
import json
import sys
sys.path.append('./')
from settings import USER, PASSWORD

# print(USER,PASSWORD)

# connect to mysql
DB_NAME = 'ezpark'
cnx = mysql.connector.connect(user=USER,
                              password=PASSWORD,
                              auth_plugin='mysql_native_password')
cursor = cnx.cursor()
cursor.execute("USE {}".format(DB_NAME))


#建立提供者

TABLES = {}
TABLES['user_order'] = (
    "CREATE TABLE `user_order` ("
    "  `order_id` INT NOT NULL AUTO_INCREMENT,"
    "  `member_id` INT NOT NULL,"
    "  `parking_space_id` INT NOT NULL,"
    "  `time_start` VARCHAR(255) DEFAULT '',"
    "  `time_end` VARCHAR(255) DEFAULT '',"
    "  `rec_trade_id` VARCHAR(255),"
    "  PRIMARY KEY (`order_id`),"
    "  FOREIGN KEY (`member_id`) REFERENCES member (`id`),"
    "  FOREIGN KEY (`parking_space_id`) REFERENCES supply (`parking_space_id`)"
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