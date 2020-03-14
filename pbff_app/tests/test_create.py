
# -*- coding: utf-8 -*-

import requests
import json
import mysql.connector

# Establishing the connection
mydb = mysql.connector.connect(
    host="localhost",
    user="sebajou_opff",
    passwd="3333argh",
    database="openfactfoods_data"
)

# Creating a cursor object using the cursor() method
cursor = mydb.cursor()

# Drop then creating table as per requirement
mycursor = mydb.cursor()

sql_key_zero = "SET FOREIGN_KEY_CHECKS=0"
sql_drop_table = "DROP TABLE IF EXISTS Food_list"
mycursor.execute(sql_key_zero)
mycursor.execute(sql_drop_table)
mycursor.execute("CREATE TABLE Food_list (id_food_code VARCHAR(100) NOT NULL PRIMARY KEY, food_name VARCHAR(100) NULL DEFAULT NULL, score_Nova_group INTEGER NULL DEFAULT NULL, nutriscore_grade CHAR(1) NULL DEFAULT NULL, food_url MEDIUMTEXT NULL DEFAULT NULL)") 
sql_key_one = "SET FOREIGN_KEY_CHECKS=1"
mycursor.execute(sql_key_one)


# Closing the connection
mydb.close()