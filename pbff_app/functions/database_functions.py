import mysql.connector


class Database:
    """All function using for the Database"""

    # Connect to database
    def connect_database(self):

        mydb = mysql.connector.connect(
            host="localhost",
            user="sebajou_opff",
            passwd="3333argh",
            database="openfactfoods_data"
        )
        # Creating a cursor object using the cursor() method
        mycursor = mydb.cursor()

        return mydb, mycursor

    # Insert data in Users table
    def insert_record_user(self, mydb, mycursor, to_insert):
        sql_record_user = "INSERT INTO Users (first_name, last_name, email, password, diet_type, alergy)VALUES(%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql_record_user, to_insert)
        mydb.commit()

    # Insert search result data in Search_food table
    def insert_search_result(self, mydb,  mycursor, to_insert):
        sql = "INSERT INTO Search_food (id_food_code, id_users) VALUES (%s, %s)"
        mycursor.execute(sql, to_insert)
        mydb.commit()

    # Show categories
    def show_categories(self, mycursor):
        mycursor.execute("SELECT DISTINCT category FROM Food_list")
        categoriesTuple = mycursor.fetchall()
        categories = list(sum(categoriesTuple, ())) 
        return categories

    # Show food_name for a given category
    def show_food_name(self, mycursor, category):
        categoryTuple = (category,)
        sql = "SELECT food_name, id_food_code FROM Food_list WHERE category = %s"
        mycursor.execute(sql, categoryTuple)
        food_name_cat_tuple = mycursor.fetchall()
        # return tuple wit food name and food id in a list
        return food_name_cat_tuple

    # Show url for OFF for a given food
    def show_food_url(self, mycursor, food_name):
        food_name = (food_name,)
        sql = "SELECT "

    # Select the healthiest food:
    def selec_healthiest_food(self, mycursor, category):
        categoryTuple = (category,)
        sql = "SELECT id_food_code, food_name, score_Nova_group, nutriscore_grade, food_url, description, store FROM Food_list WHERE category = %s ORDER BY nutriscore_grade ASC LIMIT 1"
        mycursor.execute(sql, categoryTuple)
        healthiest_food_tuple = mycursor.fetchall()
        return healthiest_food_tuple

    # Get id_user from email
    def get_id_user(self, mycursor, email):
        email_tuple = (email,)
        sql = "SELECT id_users FROM Users WHERE email = %s"
        mycursor.execute(sql, email_tuple)
        id_users_tuple = mycursor.fetchall()
        return id_users_tuple

    # Get category, food_name, id_food_code, healthiest_food_url and id_users
    # from INNER JOIN on Search_food and Food_list table
    def get_search_history_info(self, mycursor, id_users):
        id_users_tuple = (id_users,)
        sql = "SELECT Search_food.id_food_code AS id_food_code, Food_list.food_name AS food_name, \
        Food_list.food_url AS food_url, Search_food.id_users AS id_users, Food_list.category AS category, \
        Food_list.description AS description, Food_list.store AS store\
         FROM Food_list INNER JOIN Search_food ON  Search_food.id_food_code = Food_list.id_food_code WHERE id_users = %s"
        mycursor.execute(sql, id_users_tuple)
        search_history_info_tuple = mycursor.fetchall()
        return search_history_info_tuple

    # Verify email and password for connection
    def verif_connection_client(self, mycursor, email, password_hash):
        req_connection_client = "SELECT * FROM Users where email = '%s' AND password = '%s' "
        mycursor.execute(req_connection_client % (email, password_hash))
        result_connection_client = mycursor.fetchall()
        return result_connection_client

    # Control if an email is in database
    def email_exist(self, mycursor, email):
        req_user_exist = "SELECT * FROM Users WHERE Email = '%s' "
        mycursor.execute(req_user_exist % email)
        result_req_user_exist = mycursor.fetchall()
        return result_req_user_exist

    # Close the database
    def close_database(self, mydb):
        # Closing the connection of mydb
        mydb.close()
