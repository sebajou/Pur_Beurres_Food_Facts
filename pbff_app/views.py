# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify, url_for, flash, redirect, session
import json
import requests
from config import *
import mysql.connector
import hashlib, uuid, os


app = Flask(__name__)

app.config.from_object('config')

# Connection to database
mydb = mysql.connector.connect(
    host="localhost",
    user="sebajou_opff",
    passwd="3333argh",
    database="openfactfoods_data"
)
# Creating a cursor object using the cursor() method
mycursor = mydb.cursor()


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

    diet_type = ["Omnivor", "Vegan", "Vegetarian", "Carnivor", "Cannibal"]

    alergy = ['none', 'en:milk', 'en:gluten', 'en:edam-cheese', 'en:nuts',
                'en:sulphur-dioxide-and-sulphites', 'en:molluscs',
                'en:sesame-seeds', 'en:mozzarella-cheese', 'en:lupin', 'en:eggs',
                'en:fish', 'en:cajou', 'en:huile-de-beurre', 'en:celery',
                'en:soybeans', 'en:mustard', 'en:crustaceans', 'en:peanuts']


    if "e_mail" in session:
        return redirect(url_for('my_info'))

    if request.method == "GET":
        return render_template("register_user.html", diet_type=diet_type, alergy=alergy)

    if request.method == "POST":

        # Information about user
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        password_hash = hashlib.sha256(str(password).encode("utf-8")).hexdigest()
        diet_type = request.form["diet_type"]
        alergy = request.form["alergy"]

        # Control if email is not already use
        req_user_exist = "SELECT * FROM Users WHERE Email = '%s' "
        mycursor.execute(req_user_exist % email)
        result_req_user_exist = mycursor.fetchall()
        print(result_req_user_exist)

        # Message if email already use
        if len(result_req_user_exist) > 0:
            error = 'This email is already use, please use an other email'
            return render_template(
                "register_user.html", diet_type=diet_type, alergy=alergy, error = error)

        # Record user in database
        else:
            req_record_user = "INSERT INTO Users (first_name, last_name, email, password, diet_type, alergy)VALUES(%s,%s,%s,%s,%s,%s)"
            mycursor.execute(req_record_user, (first_name, last_name, email, password_hash, diet_type, alergy))
            mydb.commit()

            session["email"] = request.form["email"]

            return redirect(url_for('my_info'))

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
    mycursor = mydb.cursor()

    sql = "INSERT INTO Search_food (food_code, healthiest_food_code, id_users) VALUES (%s, %s, %s)"
    val = tuple(data)
    mycursor.execute(sql, val)

    mydb.commit()


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    session.init_app(app)

    app.debug = True
    app.run()
