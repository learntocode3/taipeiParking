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
TABLES['supply_timetable'] = (
    "CREATE TABLE `supply_timetable` ("
    "  `parking_space_id` INT NOT NULL,"
    "  `time_1_start` VARCHAR(255) NOT NULL,"
    "  `time_1_end` VARCHAR(255) NOT NULL,"
    "  `time_2_start` VARCHAR(255) NOT NULL,"
    "  `time_2_end` VARCHAR(255) NOT NULL,"
    "  `time_3_start` VARCHAR(255) NOT NULL,"
    "  `time_3_end` VARCHAR(255) NOT NULL,"
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