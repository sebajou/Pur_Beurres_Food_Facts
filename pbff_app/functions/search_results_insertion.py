import mysql.connector

def insertion(json_data_to_insert):

  #integration of json data from API OFF in list
  response = requests.get(OFF_API_URL)
  content = json.loads(response.content.decode('utf-8'))


  mydb = mysql.connector.connect(
    host="localhost",
    user="sebajou_opff",
    passwd="3333argh",
    database="openfactfoods_data"
  )

  mycursor = mydb.cursor()

  sql = "INSERT INTO Search_food (food_code, healthiest_food_code, id_users) VALUES (%s, %s, %s)"
  val = ("John", "Highway 21")
  mycursor.execute(sql, val)

  mydb.commit()