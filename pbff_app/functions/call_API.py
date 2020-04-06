# -*- coding: utf-8 -*-

# import
import requests
import json
import mysql.connector

class CallApiOff:
    """Class for call the API OFF"""

    def __init__(self):
        self.categories = ['pizza', 'pate a tartiner', 'gateau', 'choucroute', 'bonbon', 'cassoulet', 'compote', 'cookies',
                      'tartiflette', 'bolognaise']

    def append_category(self, add_category):
        """Append a new category in the category list"""

        allergens = []

        # self.categories.append(add_category)
        payload = {
            'action': 'process', 'tagtype_0': 'categories',
            'tag_contains_0': 'contains', 'tag_0': "\'" + add_category + "\'",
            'sort_by': 'unique_scans_n', 'page_size': '100',
            'axis_x': 'energy', 'axis_y': 'products_n', 'json': '1'
        }
        req = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl?", params=payload
        )
        data_json = req.json()
        print(add_category)

        for data in data_json['products']:
            try:
                if data['product_name_fr'] == '':
                    data_product_name_fr = add_category
                else:
                    data_product_name_fr = data['product_name_fr']
                data_id = int(data['id'])
                data_url = data['url']
                data_nova_group = data['nova_group']
                data_nutriscore_grade = data['nutriscore_grade']
                data_allergens = data['allergens_tags']
                data_description = data['generic_name']
                data_stores = data['stores']
            except:
                pass

            tuple_data = (
                data_id, data_product_name_fr, add_category,
                data_nova_group, data_nutriscore_grade, data_url, data_description, data_stores)

            # Loop in allergens list in each product
            for al in data_allergens:
                # Choose only english name allergens
                if al[:3] == 'en:':
                    # List all allergens in each product
                    allergens.append(al)
            # List of allergens without dooble
            allergens_list = set(allergens)

            # + Fill database tables from list

            # Connection to database
            mydb = mysql.connector.connect(
                host="localhost",
                user="sebajou_opff",
                passwd="3333argh",
                database="openfactfoods_data"
            )
            # Creating a cursor object using the cursor() method
            mycursor = mydb.cursor()

            mycursor.execute("SET FOREIGN_KEY_CHECKS=0")

            # Insertion of search result data
            mycursor = mydb.cursor()

            try:
                sql = "INSERT INTO Food_list (id_food_code, food_name, category, score_Nova_group, nutriscore_grade, food_url, description, store) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                mycursor.execute(sql, tuple_data)
                mydb.commit()
                print("inserted", add_category)
            except:
                pass

            # Insertion of search result data
            for al in data_allergens:
                if al[:3] == 'en:':
                    tuple_al = (al, data_id)
                    sql_al = "INSERT INTO Alergen (alergen_name, id_food_code) VALUES (%s, %s)"
                    mycursor.execute(sql_al, tuple_al)
                    mydb.commit()

            mycursor.execute("SET FOREIGN_KEY_CHECKS=1")

        return add_category

    def load_data(self):
        """ Loading data of the A.P.I. Open Food Facts and insertion in
        database """

        # + Drop then create Tables from API

        # Establishing the connection
        mydb = mysql.connector.connect(
            host="localhost",
            user="sebajou_opff",
            passwd="3333argh",
            database="openfactfoods_data"
        )

        # Creating a cursor object using the cursor() method
        mycursor = mydb.cursor()

        # Drop then creating tables as per requirement
        sql_key_zero = "SET FOREIGN_KEY_CHECKS=0"
        sql_drop_table_Food_list = "DROP TABLE IF EXISTS Food_list"
        sql_drop_table_Alergen = "DROP TABLE IF EXISTS Alergen"
        mycursor.execute(sql_key_zero)
        mycursor.execute(sql_drop_table_Food_list)
        mycursor.execute(sql_drop_table_Alergen)
        mycursor.execute("CREATE TABLE Food_list (id_food_code VARCHAR(100) NOT NULL PRIMARY KEY, food_name VARCHAR(100) NULL DEFAULT NULL, `category` VARCHAR(40) NULL DEFAULT NULL, score_Nova_group INTEGER NULL DEFAULT NULL, nutriscore_grade CHAR(1) NULL DEFAULT NULL, food_url MEDIUMTEXT NULL DEFAULT NULL, description VARCHAR(200) NULL DEFAULT NULL, store VARCHAR(70) NULL DEFAULT NULL)")
        mycursor.execute("CREATE TABLE `Alergen` (`id_alergen` INTEGER NOT NULL AUTO_INCREMENT, `alergen_name` VARCHAR(100) NULL DEFAULT NULL, `id_food_code` VARCHAR(100) NULL DEFAULT NULL, PRIMARY KEY (`id_alergen`))")
        sql_key_one = "SET FOREIGN_KEY_CHECKS=1"
        mycursor.execute(sql_key_one)

        # Closing the connection
        mydb.close()

        # + Fill Python list from loop on list of categories

        results = []
        allergens = []

        for elt in self.categories:
            payload = {
                'action': 'process', 'tagtype_0': 'categories',
                'tag_contains_0': 'contains', 'tag_0': "\'" + elt + "\'",
                'sort_by': 'unique_scans_n', 'page_size': '100',
                'axis_x': 'energy', 'axis_y': 'products_n', 'json': '1'
                }
            req = requests.get(
                "https://fr.openfoodfacts.org/cgi/search.pl?", params=payload
                )
            data_json = req.json()
            print(elt)

            for data in data_json['products']:
                try:
                    if data['product_name_fr'] == '':
                        data_product_name_fr = elt
                    else:
                        data_product_name_fr = data['product_name_fr']
                    data_id = int(data['id'])
                    data_url = data['url']
                    data_nova_group = data['nova_group']
                    data_nutriscore_grade = data['nutriscore_grade']
                    data_allergens = data['allergens_tags']
                    data_description = data['generic_name']
                    data_stores = data['stores']
                except:
                    pass

                tuple_data = (
                    data_id, data_product_name_fr, elt,
                    data_nova_group, data_nutriscore_grade, data_url, data_description, data_stores)

                # Loop in allergens list in each product
                for al in data_allergens:
                    # Choose only english name allergens
                    if al[:3] == 'en:':
                        # List all allergens in each product
                        allergens.append(al)
                # List of allergens without dooble
                allergens_list = set(allergens)

                # + Fill database tables from list

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
                    sql = "INSERT INTO Food_list (id_food_code, food_name, category, score_Nova_group, nutriscore_grade, food_url, description, store) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    mycursor.execute(sql, tuple_data)
                    mydb.commit()
                except:
                    pass

                # Insertion of search result data
                for al in data_allergens:
                    if al[:3] == 'en:':
                        tuple_al = (al, data_id)
                        sql_al = "INSERT INTO Alergen (alergen_name, id_food_code) VALUES (%s, %s)"
                        mycursor.execute(sql_al, tuple_al)
                        mydb.commit()

        # + Alter tables for add foreign key

        # Connect to database
        mydb = mysql.connector.connect(
            host="localhost",
            user="sebajou_opff",
            passwd="3333argh",
            database="openfactfoods_data"
        )

        # Creating a cursor object using the cursor() method
        mycursor = mydb.cursor()

        # Execute alter table command for foreign key property
        mycursor.execute("SET FOREIGN_KEY_CHECKS=0")
        mycursor.execute("ALTER TABLE `Search_food` ADD FOREIGN KEY (id_food_code) REFERENCES `Food_list` (`id_food_code`)")
        mycursor.execute("ALTER TABLE `Search_food` ADD FOREIGN KEY (id_users) REFERENCES `Users` (`id_users`)")
        mycursor.execute("ALTER TABLE `Alergy` ADD FOREIGN KEY (id_users) REFERENCES `Users` (`id_users`)")
        mycursor.execute("ALTER TABLE `Alergy` ADD FOREIGN KEY (id_alergen) REFERENCES `Alergen` (`id_alergen`)")
        mycursor.execute("ALTER TABLE `Alergen` ADD FOREIGN KEY (id_food_code) REFERENCES `Food_list` (`id_food_code`)")
        mycursor.execute("SET FOREIGN_KEY_CHECKS=1")

        mydb.commit()
        # Closing the connection
        mydb.close()

        print(allergens_list)
