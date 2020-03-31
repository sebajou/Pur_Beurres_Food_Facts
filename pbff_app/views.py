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

"""@app.before_first_request
def before_first_request_func():
    # Load the data from API
    from pbff_app.functions.call_API import load_data
    load_data()"""

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

    alergies = ['none', 'milk', 'gluten', 'edam-cheese', 'nuts',
                'sulphur-dioxide-and-sulphites', 'molluscs',
                'sesame-seeds', 'mozzarella-cheese', 'lupin', 'eggs',
                'fish', 'cajou', 'huile-de-beurre', 'celery',
                'soybeans', 'mustard', 'crustaceans', 'peanuts']

    if "email" in session:
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


# Page where we search (select) the food
@app.route('/search_food_page', methods=["GET", "POST"])
def search_food_page():

    # Obtain categories list
    categories = Database.show_categories(mycursor)

    # Give a list of food category to display in html
    if request.method == "GET":
        return render_template(
            "search_food_page.html", categories=categories)

    # Obtain selection on html form
    if request.method == "POST":
        global category_record
        category_record = request.form["category"]
        return redirect(url_for('search_food_page2'))


# Page where we search (select) the food
@app.route('/search_food_page2', methods=["GET", "POST"])
def search_food_page2():

    # Obtain tuple of food name and id for a given category and give list of food name
    food_name_cat_tuple = Database.show_food_name(mycursor, category_record)
    food_name_cat_list = [i for i, y in food_name_cat_tuple]

    # Give a list of food category
    if request.method == "GET":
        return render_template(
            "search_food_page2.html", food_name_cat_list=food_name_cat_list)

    # Obtain selection on html form
    if request.method == "POST":
        global food_name
        food_name = request.form["food_name_cat"]
        return redirect(url_for('search_food_page3'))


@app.route('/search_food_page3', methods=["GET", "POST"])
def search_food_page3():

    # Obtain the healthiest food for a given category
    # healthiest_food_name, healthiest_score_Nova_group, healthiest_nutriscore_grade, healthiest_food_url
    healthiest_food_tuple = Database.selec_healthiest_food(mycursor, category_record)
    id_food_code, healthiest_food_name, healthiest_score_Nova_group, healthiest_nutriscore_grade, healthiest_food_url = healthiest_food_tuple[0]


    if request.method == "GET":
        return render_template(
            "search_food_page3.html", category_record=category_record,
            food_name=food_name, id_food_code=id_food_code, healthiest_food_name=healthiest_food_name,
            healthiest_score_Nova_group=healthiest_score_Nova_group,
            healthiest_nutriscore_grade=healthiest_nutriscore_grade,
            healthiest_food_url=healthiest_food_url)

    if request.method == "POST":
        email = session['email']
        id_user_tuple = Database.get_id_user(mycursor, email)
        id_user, = sum(id_user_tuple, ())

        to_insert = (id_food_code, id_user)
        Database.insert_search_result(mydb, mycursor, to_insert)
        return redirect(url_for('search_food_page_history'))

# View history of search food, with link to food
@app.route("/search_food_page_history")
def search_food_page_history():

    # Obtain id_user
    email = session['email']
    id_user_tuple = Database.get_id_user(mycursor, email)
    id_user, = sum(id_user_tuple, ())

    # Obtain category, food_name, id_food_code,
    # healthiest_food_url and id_users from Search_food and Food_list table
    # id_food_code, food_name, food_url, id_users, category = Database.get_search_history_info(mycursor, id_user)
    search_history_info_tuple = Database.get_search_history_info(mycursor, id_user)

    if request.method == "GET":
        return render_template(
            "search_food_page_history.html", search_history_info_tuple=search_history_info_tuple)

"""category=category,
food_name=food_name, id_food_code=id_food_code,
food_url=food_url, id_users=id_users)"""


# For deconnection
@app.route("/to_logout")
def to_logout():
    session.pop("email", None)
    flash('Now you are logout')
    return redirect(url_for('connection'))

if __name__ == "__main__":
    session.init_app(app)
    app.debug = True
    app.run()
