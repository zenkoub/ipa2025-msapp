from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/routersdb")
client = MongoClient(mongo_uri)
db = client.get_database()
routers_collection = db.routers

@app.route("/")
def main():
    routers = list(routers_collection.find())
    return render_template("index.html", routers=routers)

@app.route("/add", methods=["POST"])
def add_comment():
    router_ip = request.form.get("router_ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if router_ip and username and password:
        routers_collection.insert_one({
            "router_ip": router_ip,
            "username": username,
            "password": password
        })
    return redirect(url_for("main"))

@app.route("/delete/<idx>", methods=["POST"])
def delete_comment(rid):
    try:
        routers_collection.delete_one({"_id": rid})
    except Exception as e:
        print("Delete error:", e)
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
