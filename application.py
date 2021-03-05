import os, json
import requests
import sqlite3
from datetime import datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloade
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Make sure API key is set
if not os.environ.get("GEOAPI_KEY"):
    raise RuntimeError("GEOAPI_KEY not set")
else:
    GEOAPI_KEY = os.environ.get("GEOAPI_KEY")

if not os.environ.get("MAP_KEY"):
    raise RuntimeError("MAP_KEY not set")
else:
    MAP_KEY = os.environ.get("MAP_KEY")

print("Connection to Database successful")
#get GEOAPI_KEY from WHOISXMLAPI
url = f"https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey={os.environ.get('GEOAPI_KEY')}"
r = requests.get(url)
j = json.loads(r.text)
lat = j['location']['lat']
lng = j['location']['lng']

def approval_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("approved") is None:
            return redirect("/approve")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
@approval_required
def form():

    if request.method == "POST":
        with sqlite3.connect("location.sqlite") as database: #COnnecting to Database
            db = database.cursor()
            print(session["approved"])

            symptoms = request.values.getlist("symptom") #gets symptoms values from form.html in a list
            vaccine = request.values.get("vaccine") #gets vaccine values from form.html
            covidTest = request.values.get("covidTest") #gets covidtest values from form.html
            riskFactor = 0 #initialize the Risk Factor

            #adds all the values/scores from the form.html and is then converted into a risk scoring for COVID 19 based on data.
            if covidTest is None:  #Converts None from covidTest to 0 to avoid errors during addition
                covidTest = 0
            riskFactor = riskFactor + int(vaccine) + int(covidTest)
            for symptom in symptoms:
                riskFactor = riskFactor + int(symptom)

            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #put all derived data from form.html to an SQL database.
            addData = db.execute("INSERT INTO location (lat, lng, date, risk) VALUES (?, ?, ?, ?)",
            (lat, lng , time, riskFactor))


            session['time'] = time
        return redirect(url_for('maps'))
    else:
        return render_template("form.html")


@app.route("/maps")
@approval_required
def maps():
    with sqlite3.connect("location.sqlite") as database:
        db = database.cursor()
        #select all locations from database from within 2 weeks ago
        locationsCursor = db.execute("SELECT lat, lng, risk FROM location WHERE julianday('now') - julianday(date) <= 14 ;")
        print(session["approved"])
        print(locationsCursor)
        #iniate to lists for lat and lng to be sent to HTML & JS
        locations_lat = list()
        locations_lng = list()
        locations_risk = list()
        riskScore = 0
        #adds lat, lng, and risk to respective lists from SQL cursor
        for location in locationsCursor:
            locations_lat.append(location[0])
            locations_lng.append(location[1])
            locations_risk.append(location[2])

        #fetches Risk Score of the current user
        riskCursor = db.execute("SELECT risk FROM location WHERE date=?", (session['time'],))
        # assigns Risk Score of current user to locations_risk variable
        for risk in riskCursor:
            riskScore = risk[0]

    session.clear()
    #convert list to json format to be sent to maps.html and render template based on riskScore
    if riskScore <= 3:
            return render_template("maps_safe.html", MAP_KEY = MAP_KEY, locations_lat = json.dumps(locations_lat), locations_lng = json.dumps(locations_lng), locations_risk = json.dumps(locations_risk), riskScore = riskScore, user_lat = lat, user_lng = lng)
    elif riskScore > 3 and riskScore <= 7:
            return render_template("maps_risky.html", MAP_KEY = MAP_KEY, locations_lat = json.dumps(locations_lat), locations_lng = json.dumps(locations_lng), locations_risk = json.dumps(locations_risk), riskScore = riskScore, user_lat = lat, user_lng = lng)
    else:
            return render_template("maps_covid.html", MAP_KEY = MAP_KEY, locations_lat = json.dumps(locations_lat), locations_lng = json.dumps(locations_lng), locations_risk = json.dumps(locations_risk), riskScore = riskScore, user_lat = lat, user_lng = lng)


@app.route("/approve" , methods =["GET", "POST"])
def approve():
    #gets user consent for logging location

    session.clear() #forgets any previous session

    if request.method == "POST":
        session["approved"] = 1
        return redirect("/")
    else:
        return render_template("approve.html")

