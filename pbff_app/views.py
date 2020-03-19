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
