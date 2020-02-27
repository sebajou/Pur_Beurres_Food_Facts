# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, url_for
import json
import requests
from config import *
import mysql.connector


app = Flask(__name__)

app.config.from_object('config')

@app.route("/")
def hello():
    return "Hello World!"

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


if __name__ == "__main__":
    app.run()