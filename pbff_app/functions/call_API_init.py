# -*- coding: utf-8 -*-

# import
import requests
import json
import mysql.connector

allergens = []

class CallAPI:
    """ Call A.P.I. Open Food Facts """

    

    def load_data(self):
        """ Loading data of the A.P.I. Open Food Facts and convert to json """

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
        mycursor.execute("CREATE TABLE Food_list (id_food_code VARCHAR(100) NOT NULL PRIMARY KEY, food_name VARCHAR(100) NULL DEFAULT NULL, `category` VARCHAR(40) NULL DEFAULT NULL, score_Nova_group INTEGER NULL DEFAULT NULL, nutriscore_grade CHAR(1) NULL DEFAULT NULL, food_url MEDIUMTEXT NULL DEFAULT NULL)") 
        sql_key_one = "SET FOREIGN_KEY_CHECKS=1"
        mycursor.execute(sql_key_one)

        # Closing the connection
        mydb.close()

        # ...
        categories = ['pizza', 'pate a tartiner', 'gateau', 'choucroute', 'bonbon', 'cassoulet', 'compote']
        results = []

        for elt in categories:
            payload = {'action': 'process', 'tagtype_0': 'categories', 'tag_contains_0': 'contains',
                    'tag_0': "\'" + elt + "\'", 'sort_by': 'unique_scans_n', 'page_size': '100',
                    'axis_x': 'energy', 'axis_y': 'products_n', 'json': '1'}
            req = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)
            data_json = req.json()

            # data_str = json.dumps(data_json, indent = 2) 

            for data in data_json['products']:
                try:
                    data_product_name_fr = data['product_name_fr']
                    data_id = int(data['id'])
                    data_url = data['url']
                    data_nova_group = data['nova_group']
                    data_nutriscore_grade = data['nutriscore_grade']
                    data_allergens = data['allergens_tags']
                except:
                    pass

                dic_data = {"data_id": data_id, "data_product_name_fr": data_product_name_fr,
                        "data_category": elt,
                        "data_nova_group": data_nova_group, "nutriscore_grade": data_nutriscore_grade, "data_url": data_url}
                tuple_data = (data_id, data_product_name_fr, elt, data_nova_group, data_nutriscore_grade, data_url)
                results.append(dic_data)

                for al in data_allergens:
                    if al[:3] == 'en:':
                        allergens.append(al)

                allergens_list = set(allergens)
                # allergens.append(data_allergens)

                # Connection to database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="sebajou_opff",
                    passwd="3333argh",
                    database="openfactfoods_data"
                )

                # Insertion of search result data
                mycursor = mydb.cursor()

                try:
                    sql = "INSERT INTO Food_list (id_food_code, food_name, category, score_Nova_group, nutriscore_grade, food_url) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = tuple_data
                    mycursor.execute(sql, val)

                    mydb.commit()
                except:
                    pass

        print(allergens_list)

Call = CallAPI()
Call.load_data()

