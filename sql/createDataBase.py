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

# Create datebase if not exist
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)
