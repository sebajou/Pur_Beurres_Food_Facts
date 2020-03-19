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

    # Insertion of search result data
    def insert_search_result(self, mydb, data):
        """mycursor = mydb.cursor()
        sql = "INSERT INTO Search_food (food_code, healthiest_food_code, id_users) VALUES (%s, %s, %s)"
        val = tuple(data)
        mycursor.execute(sql, val)
        mydb.commit()"""
        pass

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
