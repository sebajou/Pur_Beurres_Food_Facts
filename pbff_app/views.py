# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify, url_for, flash, redirect, session
import json
import requests
from config import *
import hashlib, uuid, os
import pbff_app.functions.database_functions as db

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = the_secret_key

# Instanciation of database_functions
Database = db.Database()
# Connection to database
mydb, mycursor = Database.connect_database()


@app.route('/')
def index():
    if "email" in session:
        return redirect(url_for('my_info'))
    else:
        return render_template("/connect.html")

# View where user is register
@app.route("/register_user", methods=["GET", "POST"])
def register_user():

    error = None

    diet_types = ["Omnivor", "Vegan", "Vegetarian", "Carnivor", "Cannibal"]

    alergies = ['none', 'en:milk', 'en:gluten', 'en:edam-cheese', 'en:nuts',
                'en:sulphur-dioxide-and-sulphites', 'en:molluscs',
                'en:sesame-seeds', 'en:mozzarella-cheese', 'en:lupin', 'en:eggs',
                'en:fish', 'en:cajou', 'en:huile-de-beurre', 'en:celery',
                'en:soybeans', 'en:mustard', 'en:crustaceans', 'en:peanuts']

    if "e_mail" in session:
        return redirect(url_for('my_info'))

    if request.method == "GET":
        return render_template(
            "register_user.html", diet_types=diet_types, alergies=alergies)

    if request.method == "POST":
        # Information about user
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        password_hash = hashlib.sha256(str(password).encode("utf-8")).hexdigest()
        diet_type_record = request.form["diet_type"]
        alergy_record = request.form["alergy"]

        # Control if email is not already use
        result_req_user_exist = Database.email_exist(mycursor, email)
        print(result_req_user_exist)
        # Message if email already use
        if len(result_req_user_exist) > 0:
            error = 'This email is already use, please use an other email'
            return render_template(
                "register_user.html", error=error, diet_types=diet_types,
                alergies=alergies)

        # Record user in database
        else:
            to_insert = (
                first_name, last_name, email, password_hash,
                diet_type_record, alergy_record)
            Database.insert_record_user(mydb, mycursor, to_insert)
            session["email"] = request.form["email"]
            
            return redirect(url_for('my_info'))

# View for connection
@app.route("/connection", methods=["GET", "POST"])
def connection():
    error = None

    if request.method == "POST":
        email = request.form["email"]

        password = request.form["password"]
        password_hash = hashlib.sha256(str(password).encode("utf-8")).hexdigest()

        # Verify in database if email and password exist
        result_connection_client = Database.verif_connection_client(mycursor, email, password_hash)

        if len(result_connection_client) == 0:
            session['email'] = None
            error = "This email or this password is wrong, please try again"
            return render_template("connection.html", error=error)

        else:
            session["email"] = request.form["email"]
            return redirect(url_for('my_info'))

    elif request.method == "GET":
        return render_template("connection.html")

# Print the account information
@app.route("/my_info", methods=["GET", "POST"])
def my_info():
    if request.method == "GET" and "email" in session:
        email = session["email"]
        req_get_id_user = "SELECT id_users FROM Users WHERE email = '%s'"
        mycursor.execute(req_get_id_user % email)
        id_users = mycursor.fetchone()

        req_info_users = "SELECT Users.first_name, Users.last_name, Users.email, Users.diet_type, Users.alergy FROM Users WHERE Users.email = '%s'"
        mycursor.execute(req_info_users % email)
        result_req_info_users = mycursor.fetchall()

        # print(result_req_info_users)
        return render_template("/my_info.html",
                               result_req_info_users=result_req_info_users)

    if request.method == "POST":
        email = session["email"]

        req_get_id_users = "SELECT id_users FROM Users WHERE Email = '%s'"
        mycursor.execute(req_get_id_users % e_mail)
        id_users = mycursor.fetchone()

        return redirect(url_for('my_info'))
    else :
        return redirect(url_for('connection'))

@app.route('/search_food_page/')
def search_food_page():
    #integration of json data from API OFF in list
    response = requests.get(OFF_API_URL)
    content = json.loads(response.content.decode('utf-8'))

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'API request fail. See the message : {}'.format(content['message'])
        }), 500

    data = []
    for prev in content["list"]:
        food_code = prev['xxxx']
        healthiest_food_code = prev['yyyy']
        id_users = zzzz

    return jsonify({
      'status': 'ok',
      'data': data
    })

    # Insertion of search result data



if __name__ == "__main__":
    session.init_app(app)
    app.debug = True
    app.run()
