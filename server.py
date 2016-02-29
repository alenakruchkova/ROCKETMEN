"""Rocketmen"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, jsonify, json
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Astronaut, Country
from helper import get_people_in_space_info, lookup_id_from_name, current_flight_duration, look_up_flag, get_current_iss_location
from helper import get_lat_lng, get_next_iss_pass_for_lat_lng

from googlemaps import Client
from datetime import datetime
import requests
import os
import sys


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# Raises an error if undentified variable is used in Jinja2
#  (otherwise Jinja fails scilently)
app.jinja_env.undefined = StrictUndefined

######################################################################


@app.route('/')
def get_seed_info():
    """Show landing page"""

    return render_template("index.html")


@app.route('/home')
def index():
    """Homepage."""
    # Get data from API
    jdict = get_people_in_space_info()

    # Number of people in space from JSON data
    num_result = jdict['number']

    # COLLECT list of names like ["Michael Kornienko", "Sergey Vokov",...] from JSON data
    name_list = [p['name'] for p in jdict['people']]

    # DB astronauts table query for names in name_list
    list_astro_obj = db.session.query(Astronaut).filter(Astronaut.name.in_(name_list)).all()

    # Dictionary with all names from API request and corresponding ids from db
    name_id = {name: lookup_id_from_name(name, list_astro_obj) for name in name_list}

    return render_template("home.html",
                            num_result=num_result,
                            name_id=name_id)


@app.route("/astronauts/<int:astronaut_id>")
def show_astronaut_info(astronaut_id):
    """Show information about the astronaut"""

    #Query astronauts table on astronaut_id
    astronaut = Astronaut.query.filter(Astronaut.astronaut_id == astronaut_id).one()

    flag = look_up_flag(astronaut)
    days = current_flight_duration(astronaut)

    return render_template("astronaut.html",
                            flag=flag,
                            days=days,
                            **astronaut.__dict__)


@app.route('/iss')
def iss_page():
    """Show information about ISS"""

    jdict = get_current_iss_location()

    lat = jdict["iss_position"]["latitude"]
    lng = jdict["iss_position"]["longitude"]

    return render_template("iss.html",
                            lat=lat,
                            lng=lng)


@app.route('/iss-pass', methods=['GET'])
def get_iss_pass_result():
    """Get duration and time for the next ISS pass for user input location"""

    jdict = get_next_iss_pass_for_lat_lng()

    pass_duration = jdict["response"][0]["duration"]
    pass_datetime = jdict["response"][0]["risetime"]

    pass_datetime = datetime.fromtimestamp(int(pass_datetime)).strftime('%Y-%m-%d %H:%M:%S')

    iss_pass = {'duration': pass_duration,
                'date_time': pass_datetime}

    return jsonify(iss_pass)


######################################################################

# ROUTES TESTING API CALLS

@app.route('/astros.json')
def astronauts_info():
    """JSON info about people in space right now."""

    jdict = requests.get("http://api.open-notify.org/astros.json")
    jdict = jdict.json()

    return jsonify(jdict)


@app.route('/iss-pass.json')
def iss_pass_info():
    """JSON with timestamp and duration in seconds
    for the next passing of ISS for specific location."""

    payload = {'lat': 37,
               'lon': 122 }
    jdict = requests.get("http://api.open-notify.org/iss-pass.json", params=payload)
    jdict = jdict.json()

    return jsonify(jdict)


@app.route('/iss-now.json')
def iss_now_info():
    """JSON with current lat and lng of ISS"""

    jdict = requests.get("http://api.open-notify.org/iss-now.json")
    jdict = jdict.json()

    return jsonify(jdict)


######################################################################

if __name__ == "__main__":
    # debug=True , since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run()
