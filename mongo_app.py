from flask import Flask, render_template, redirect, url_for, session, flash
import pymongo, requests, random


mongo_app = Flask(__name__)

connection = pymongo.MongoClient("homer.stuy.edu")
connection.drop_database("freudenbergJ-zorinM")
client = connection["freudenbergJ-zorinM"]
# client.drop_database("freudenbergJ-zorinM")
movies = client["movies"]

r = requests.get("https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json")
data = r.json()

for doc in data:
    movies.insert_one(doc)

@mongo_app.route('/')
def root():
    return render_template("base.html")

@mongo_app.route('/answer')
def answer():
    director = request.form['director']
    direct_cursor = movies.find({"director" : director})
    L = list()
    for movie in direct_cursor:
        L.append(movie)
    flash(random.choice(L))
    return render_template("base.html")


if __name__ == "__main__":
    mongo_app.run(debug = True)
