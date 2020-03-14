"""import requests

categories = ['pizza', 'pate a tartiner', 'gateau', 'yaourt', 'bonbon']
list_data = []

for elt in categories:
    payload = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains',
               'tag_0': "\'" + elt + "\'", 'sort_by': 'unique_scans_n', 'page_size': '1000',
               'axis_x': 'energy', 'axis_y': 'products_n', 'json': '1'}
    req = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)
    data = req.json()
    list_data.append(data)

#################

import requests
import json

results = []

payload = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains',
        'tag_0': "\'" + 'choucroute' + "\'", 'sort_by': 'unique_scans_n', 'page_size': '100',
        'axis_x': 'energy', 'axis_y': 'products_n', 'json': '1'}
req = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)
data = req.json()
data_str = json.dumps(data, indent = 2)

data_id = data['products'][0]['id']
data_product_name_fr = data['products'][0]['product_name_fr']
data_url = data['products'][0]['url']
data_nova_group = data['products'][0]['nova_group']

dic_data = {"data_id": data_id,"data_product_name_fr": data_product_name_fr, "data_url": data_url, "data_nova_group": data_nova_group}

results.append(dic_data)"""


#################
"""# -*- coding: utf-8 -*-

import requests
import json

categories = ['pizza', 'pate a tartiner', 'gateau', 'choucroute', 'bonbon']

results = []

for elt in categories:
    payload = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains',
            'tag_0': "\'" + elt + "\'", 'sort_by': 'unique_scans_n', 'page_size': '100',
            'axis_x': 'energy', 'axis_y': 'products_n', 'json': '1'}
    req = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)
    data = req.json()
    data_str = json.dumps(data, indent = 2) 
    data_id = data['products'][0]['id']
    data_product_name_fr = data['products'][0]['product_name_fr']
    data_url = data['products'][0]['url']
    data_nova_group = data['products'][0]['nova_group']
    dic_data = {"data_id": data_id,"data_product_name_fr": data_product_name_fr, 
            "data_url": data_url, "data_nova_group": data_nova_group}
    results.append(dic_data)
    print(results)

    https://fr.openfoodfacts.org/cgi/search.pl?search_terms=choucroute&search_simple=1&action=process
"""

"""
#Connection to database
mydb = mysql.connector.connect(
    host="localhost",
    user="sebajou_opff",
    passwd="3333argh",
    database="openfactfoods_data"
)

#Insertion of search result data
mycursor = mydb.cursor()

sql = "INSERT INTO Search_food (food_code, healthiest_food_code, id_users) VALUES (%s, %s, %s)"
val = tuple(data)
mycursor.execute(sql, val)

mydb.commit()
"""
################

# -*- coding: utf-8 -*-

import requests
import json
import mysql.connector


"""# Delete old database Food_list
mydb = mysql.connector.connect(
    host="localhost",
    user="sebajou_opff",
    passwd="3333argh",
    database="openfactfoods_data"
)
mycursor = mydb.cursor()
sql_drop = "SET FOREIGN_KEY_CHECKS=0; DROP TABLE IF EXISTS Food_list; SET FOREIGN_KEY_CHECKS=1"
mycursor.execute(sql_drop, multi=True)

# Create new Food_list database
mydb = mysql.connector.connect(
    host="localhost",
    user="sebajou_opff",
    passwd="3333argh",
    database="openfactfoods_data"
)
mycursor = mydb.cursor()
sql_create = "CREATE TABLE Food_list (id_food_code VARCHAR(100) NOT NULL PRIMARY KEY, food_name VARCHAR(100) NULL DEFAULT NULL, score_Nova_group INTEGER NULL DEFAULT NULL, nutriscore_grade CHAR(1) NULL DEFAULT NULL, food_url MEDIUMTEXT NULL DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8"
mycursor.execute(sql_create, multi=True)
"""

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

# ...
categories = ['pizza', 'pate a tartiner', 'gateau', 'choucroute', 'bonbon', 'cassoulet', 'couscous']
results = []


for elt in categories:
    payload = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains',
            'tag_0': "\'" + elt + "\'", 'sort_by': 'unique_scans_n', 'page_size': '100',
            'axis_x': 'energy', 'axis_y': 'products_n', 'json': '1'}
    req = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)
    data_json = req.json()

    data_str = json.dumps(data_json, indent = 2) 

    for data in data_json['products']:
        try:
            data_product_name_fr = data['product_name_fr']
            data_id = int(data['id'])
            data_url = data['url']
            data_nova_group = data['nova_group']
            data_nutriscore_grade = data['nutriscore_grade']
        except:
            pass

        dic_data = {"data_id": data_id,"data_product_name_fr": data_product_name_fr, 
                "data_nova_group": data_nova_group, "nutriscore_grade": data_nutriscore_grade, "data_url": data_url}
        tuple_data = (data_id, data_product_name_fr, data_nova_group, data_nutriscore_grade, data_url)
        results.append(dic_data)


        #Connection to database
        mydb = mysql.connector.connect(
            host="localhost",
            user="sebajou_opff",
            passwd="3333argh",
            database="openfactfoods_data"
        )

        #Insertion of search result data
        mycursor = mydb.cursor()

        try:
            sql = "INSERT INTO Food_list (id_food_code, food_name, score_Nova_group, nutriscore_grade, food_url) VALUES (%s, %s, %s, %s, %s)"
            val = tuple_data
            mycursor.execute(sql, val)

            mydb.commit()
        except:
            pass
