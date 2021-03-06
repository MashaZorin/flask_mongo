from flask import Flask, render_template, redirect, url_for, request, session, flash
import pymongo, requests, random, os



mongo_app = Flask(__name__)
mongo_app.secret_key = os.urandom(64)

connection = pymongo.MongoClient("homer.stuy.edu")
connection.drop_database("freudenbergJ-zorinM")
print "Dropped database"
client = connection["freudenbergJ-zorinM"]
movies = client["movies"]

r = requests.get("https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json")
data = r.json()

print "Adding movies to db... (will take a while)"

for doc in data:
    movies.insert_one(doc)

print "Added movies"

@mongo_app.route('/')
def root():
    return render_template("base.html")

@mongo_app.route('/answer', methods = ['GET','POST'])
def answer():
    director = request.form['director']
    direct_cursor = movies.find({"director" : director})
    L = list()
    for movie in direct_cursor:
        L.append(movie)
    flash(random.choice(L))
    return render_template("base.html")


if __name__ == "__main__":
    mongo_app.run(debug = True, use_reloader=False)
