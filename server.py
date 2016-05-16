"""Rocketmen"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, session, jsonify, json
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Astronaut, Country
from helper import get_people_in_space_info, lookup_id_from_name, current_flight_duration, look_up_flag, get_current_iss_location
from helper import get_lat_lng, get_next_iss_pass_for_lat_lng

from sqlalchemy import func

import random

from googlemaps import Client
from datetime import datetime
import requests
import os
import sys

PORT = int(os.environ.get("PORT", 5000))


app = Flask(__name__)

DEBUG = "NO_DEBUG" not in os.environ

# Required to use Flask sessions and the debug toolbar
SECRET_KEY = "ABC"

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "ABC")

app.secret_key = "ABC"
# Raises an error if undentified variable is used in Jinja2
#  (otherwise Jinja fails scilently)
app.jinja_env.undefined = StrictUndefined

######################################################################

@app.route("/error")
def error():
    raise Exception("Error!")

@app.route('/')
def get_seed_info():
    """Show landing page"""

    return render_template("index.html")

@app.route('/about')
def about_rocketmen():
    """Info about project"""

    return render_template("about.html")

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
    # Get data from isss-now API
    jdict = get_current_iss_location()

    lat = jdict["iss_position"]["latitude"]
    lng = jdict["iss_position"]["longitude"]

    return render_template("iss.html",
                            lat=lat,
                            lng=lng)


@app.route('/iss-pass', methods=['GET'])
def get_iss_pass_result():
    """Get duration and time for the next ISS pass for user input location"""
    # Get data from iss-pass API
    jdict = get_next_iss_pass_for_lat_lng()

    pass_duration = jdict["response"][0]["duration"]
    pass_datetime = jdict["response"][0]["risetime"]

    # Convert timestamp into date/time string
    pass_datetime = datetime.fromtimestamp(int(pass_datetime)).strftime('%Y-%m-%d %H:%M:%S')

    iss_pass = {'duration': pass_duration,
                'date_time': pass_datetime}

    return jsonify(iss_pass)


@app.route('/stats')
def get_stats_all_human_flights():
    """Show charts and graphs representing all human space flights"""

    return render_template("stats.html")


@app.route('/get-gender-chart.json')
def get_gender_chart():
    """Query database and generate data for gender chart"""

    male_count = db.session.query(Astronaut).filter_by(gender='M').count()
    # male_count = Astronaut.query.filter(Astronaut.gender == 'M').count()
    # print male_count
    astronaut = Astronaut.query.filter(Astronaut.astronaut_id == astronaut_id).one()
    # female_count = Astronaut.query.filter(Astronaut.gender == 'F').count()

    data_list_of_dicts = {
        'astronauts': [
            {
                "value": int(male_count),
                "color": "#58d2d3",
                "highlight": "#86dfdf",
                "label": "Male"
            },
            {
                "value": int(female_count),
                "color": "#f4719d",
                "highlight": "#fab8ce",
                "label": "Female"
            },
        ]
    }
    return jsonify(data_list_of_dicts)


@app.route('/get-decade-chart.json')
def get_decade_chart():
    """Query database and generate data for decade chart"""

    astronauts = db.session.query(Astronaut).all()

    sixties = 0
    seventies = 0
    eighties = 0
    nineties = 0
    twothounds = 0
    twothousandtens = 0

    for astronaut in astronauts:
        year = int(astronaut.first_flight_start[-4:])
        if year > 2009:
            twothousandtens += 1
        elif year > 1999:
            twothounds += 1
        elif year > 1989:
            nineties += 1
        elif year > 1979:
            eighties += 1
        elif year > 1969:
            seventies += 1
        else:
            sixties += 1

        data_list_of_dicts = {
            'labels': ["1960", "1970", "1980", "1990", "2000", "2010"],
            'datasets': [
                {
                    "fillColor": "#a5f5f6",
                    "strokeColor": "#1b969e",
                    "pointColor": "#0b3e41",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                    "data": [int(sixties), int(seventies), int(eighties), int(nineties), int(twothounds), int(twothousandtens)]
                }
            ]
        }

    return jsonify(data_list_of_dicts)


@app.route('/get-nat-chart.json')
def get_nat_chart():
    """Query database and generate data for decade chart"""

    # Query db for astronauts by country
    nat_count = db.session.query(func.count(Astronaut.country_id), Country.name).join(Country).group_by(Country.name).all()

    # Create nat_dict {"country": number of astronauts}.
    # Combine counts for countries with less then 10 flights under key "other"
    nat_dict = {"other": 0}
    for tupel in nat_count:
        if tupel[0] > 9:
            nat_dict[tupel[1]] = tupel[0]
        else:
            nat_dict["other"] += tupel[0]

    # Combine counts for Russia and Soviet Union
    nat_dict["Russian Federation"] += nat_dict["Soviet Union"]
    del nat_dict["Soviet Union"]

    color = ["#1b969e", "#f75e24", "#58d2d3", "#fcd9a0", "#a5f5f6", "#fed65a"]
    highlight = ["#25ceda", "#fa916b", "#86dfdf", "#fef5e6", "#e8fcfd", "#fee59a"]

    image = ["../img/counter-1.png", "../img/counter-2.png", "../img/counter-3.png", "../img/counter-4.png", "../img/counter-5.png", "../img/counter-6.png"]

    list_of_dicts = []

    data_list_of_dicts = {
        'astronauts': list_of_dicts}

    i = 0
    for item in nat_dict:
        list_of_dicts.append({
                "value": int(nat_dict[item]),
                "color": str(color[i]),
                "highlight": str(highlight[i]),
                "label": str(item),
            })
        i += 1

    return jsonify(data_list_of_dicts)


@app.route('/get-numflights-chart.json')
def get_num_flights_chart():
    """Query database and generate data for number of flights chart"""

    # desc order vvvvv

    # flight_count = db.session.query(func.count(Astronaut.num_completed_flights),
    #     Astronaut.num_completed_flights).group_by(Astronaut.num_completed_flights).all()

    # num_flight_dict = {}
    # for tupel in flight_count:
    #     num_flight_dict[tupel[1]] = tupel[0]

    one = db.session.query(Astronaut).filter(Astronaut.num_completed_flights == 1).count()
    two = db.session.query(Astronaut).filter(Astronaut.num_completed_flights == 2).count()
    three = db.session.query(Astronaut).filter(Astronaut.num_completed_flights == 3).count()
    four = db.session.query(Astronaut).filter(Astronaut.num_completed_flights == 4).count()
    five = db.session.query(Astronaut).filter(Astronaut.num_completed_flights == 5).count()
    six = db.session.query(Astronaut).filter(Astronaut.num_completed_flights == 6).count()
    seven = db.session.query(Astronaut).filter(Astronaut.num_completed_flights == 7).count()

    data_list_of_dicts = {
        'labels': ["1", "2", "3", "4", "5", "6", "7"],
        'datasets': [
            {
                "fillColor": "rgba(220,220,220,0.5)",
                "data": [int(one), int(two), int(three), int(four), int(five), int(six), int(seven)]
            }
        ]
    }

    return jsonify(data_list_of_dicts)

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
               'lon': 122}
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

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
