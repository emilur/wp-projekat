import datetime
import pymysql
import flask
from flask import Flask
from flaskext.mysql import MySQL
from flask import request


app = Flask(__name__, static_url_path="")


mysql = MySQL(cursorclass=pymysql.cursors.DictCursor)

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "1234"
app.config["MYSQL_DATABASE_DB"] = "real_estates"
app.config["MYSQL_DATABASE_HOST"] = "localhost"

mysql.init_app(app)

@app.route('/')
@app.route('/log')
def log():
    return app.send_static_file('logIn.html')

@app.route("/index")
@app.route("/index.html")
@app.route('/home')
def home():   
    return app.send_static_file("index.html")




@app.route("/realestate", methods=["GET"])
def nekretnine():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM realestate")
    rows = cursor.fetchall()  

    return flask.jsonify(rows)


@app.route("/realestate/<int:id>", methods=["GET"])
def nekretnina(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM realestate WHERE id=%s", (id, ))
    row = cursor.fetchone()

    return flask.jsonify(row)

@app.route("/realestate", methods=["POST"])
def dodaj_nekretninu():
    data = request.json
    db = mysql.get_db()
    cursor = db.cursor()

    q = '''INSERT INTO
    realestate(title, location, price, other_info, image_src)
    VALUES(%s, %s, %s, %s, %s)'''

    cursor.execute(q, (data["title"], data["location"], data["price"],
                       data["other_info"], data["image_src"]))
    db.commit()
    return flask.jsonify({"status": "done"}), 201

@app.route("/realestate/<int:id>", methods=["DELETE"])
def ukloni_nekretninu(id):
    db = mysql.get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM realestate WHERE id=%s", (id, ))
    db.commit()

    return ""

@app.route("/realestate/<int:id>", methods=["PUT"])
def izmeni_nekretninu(id):
    data = request.json
    db = mysql.get_db()
    cursor = db.cursor()
    q = '''UPDATE realestate SET title=%s, location=%s, price=%s,
    other_info=%s, image_src=%s WHERE id=%s'''

    cursor.execute(q, (data["title"], data["location"], data["price"],
                       data["other_info"], data["image_src"], id))
    db.commit()
    
    return ""


app.run("0.0.0.0", 80, threaded=True, debug=True)
