from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    # first run doesn't return anything because nothing has been scraped yet.
    mars_facts = mongo.db.mars_facts.find_one()
    return render_template("index.html", mars_facts=mars_facts)

@app.route("/scrape")
def scraper():
    # creates collection connection
    mars_facts = mongo.db.mars_facts
    # variable that stores scraped information from scrape function.
    mars_data = scrape_mars.scrape()
    mars_facts.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)