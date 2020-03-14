# -*- coding: utf-8 -*-

import requests
import json
import mysql.connector


# Delete old database Food_list
mydb = mysql.connector.connect(
    host="localhost",
    user="sebajou_opff",
    passwd="3333argh",
    database="openfactfoods_data"
)
mycursor = mydb.cursor()

sql_key_zero = "SET FOREIGN_KEY_CHECKS=0"
sql_drop_table = "DROP TABLE IF EXISTS Food_list"
sql_key_one = "SET FOREIGN_KEY_CHECKS=1"
mycursor.execute(sql_key_zero)
mycursor.execute(sql_drop_table)
mycursor.execute(sql_key_one)

