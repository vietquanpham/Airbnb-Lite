from flask import Flask, Response, request, jsonify
from flask_pymongo import pymongo
from database import DatabaseConnection
import datetime

app = Flask(__name__)
db = DatabaseConnection()

@app.route("/addNewProperty", methods=["POST"])
def addNewProperty():
    document = {
        "name": request.form["name"],
        "propertyType": request.form["type"],
        "price": request.form["price"]
    }
    db.insert("properties", document)
    return Response("Property succesfully added", status=200, content_type="text/html")

@app.route("/properties", methods=["GET"])
def getProperties():
    properties = db.findMany("properties", {})
    return jsonify(properties)

@app.route("/", methods=["GET"])
def hello():
    return Response("<h1> Hey there </h1>", status=200, content_type="text/html")

@app.route("/greeting", methods=["POST"])
def greeting():
    name = request.form["name"]
    hourOfDay = datetime.datetime.now().time().hour
    greeting = ""
    if not name:
        return Response(status=404)
    if hourOfDay < 12: 
        greeting = "Good morning "
    elif hourOfDay >= 12 and hourOfDay < 18:
        greeting = "Good afternoon "
    else:
        greeting = "Good evening " 
    response = greeting + " " + name + "!"
    return Response(response, status=200, content_type="text/html")

if __name__ == "__main__":
    app.run(host="localhost", port=4000, debug=True)