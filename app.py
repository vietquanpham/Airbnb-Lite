from flask import Flask, Response, request, jsonify, render_template, session, redirect, url_for
from flask_pymongo import pymongo
from database import DatabaseConnection
import datetime, bcrypt

app = Flask(__name__)
db = DatabaseConnection()

@app.route("/add_new_property", methods=["POST"])
# vendor mode: add a new property
def add_new_property(): 
    document = {
        "name": request.form["name"],
        "propertyType": request.form["type"],
        "price": request.form["price"]
    }
    db.insert("properties", document)
    return Response("Property succesfully added", status=200, content_type="text/html")

@app.route("/properties", methods=["GET"])
# both vendor and renter: get a list of properties 
def get_properties():
    properties = db.findMany("properties", {})
    return jsonify(properties)

@app.route("/", methods=["GET"])
# home page 
def index():
    #return Response("<h1> Hey there </h1>", status=200, content_type="text/html")
    # check if the user is logged in, if not pull up log in form
    if "username" in session:
        return "You are logged in as " + session["username"]
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    login_user = db.findOne("users", {"name": request.form["username"]})
    if login_user:
        # check if password is correct
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        existing_user = db.findOne("users", {"name": request.form["username"]})
        # if username is not in db, create new user
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form["pass"].encode("utf-8"), bcrypt.gensalt())
            db.insert("users", {"name": request.form["username"], "password": hashpass})
            session["username"] = request.form["username"]
            return redirect(url_for("index"))
        return "The username already exists"
    
    return render_template("register.html")

@app.route("/greeting", methods=["POST"])
def greeting(): 
    name = request.form["name"]
    hour_of_day = datetime.datetime.now().time().hour
    greeting = ""
    if not name:
        return Response(status=404)
    if hour_of_day < 12: 
        greeting = "Good morning "
    elif hour_of_day >= 12 and hour_of_day < 18:
        greeting = "Good afternoon "
    else:
        greeting = "Good evening " 
    response = greeting + " " + name + "!"
    return Response(response, status=200, content_type="text/html")

if __name__ == "__main__":
    app.secret_key = "secretkey"
    app.run(host="localhost", port=4000, debug=True)