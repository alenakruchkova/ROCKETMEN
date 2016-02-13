"""Rocketmen"""

from datetime import datetime

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, session, jsonify, json
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Astronaut, Country

import requests

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# Raises an error if undentified variable is used in Jinja2
#  (otherwise Jinja fails scilently)
app.jinja_env.undefined = StrictUndefined

############################################################################

@app.route('/')
def get_seed_info():
    """Show landing page"""

    return render_template("index.html")


@app.route('/home')
def index():
    """Homepage."""
    # Get data from API
    jdict = requests.get("http://api.open-notify.org/astros.json")
    jdict = jdict.json()

    # Number of people in space
    num_result = jdict['number']

    # Dictionary with name-id key-value pairs
    name_id = {}

    # List of names of people in space

    name_list = [p['name'] for p in jdict['people']]
    name_id = [{p['name']: None} for p in jdict['people']]

    # Get astronaut ids by name:
    for name in name_list:
        astronaut_obj = db.session.query(Astronaut).filter(Astronaut.name == name).first()
        if astronaut_obj:
            astronaut_id = astronaut_obj.astronaut_id
            name_id[name] = astronaut_id

    # astronaut_obj_list = db.session.query(Astronaut).filter(Astronaut.name in name_list).all()


    return render_template("home.html",
                            num_result=num_result,
                            name_id=name_id)


@app.route('/astros.json')
def astronauts_info():
    """JSON info about people in space right now."""

    jdict = requests.get("http://api.open-notify.org/astros.json")
    jdict = jdict.json()


    return jsonify(jdict)


@app.route("/astronauts/<int:astronaut_id>")
def show_astronaut_info(astronaut_id):
    """Show information about the astronaut"""

    astronaut = Astronaut.query.filter(Astronaut.astronaut_id == astronaut_id).one()

    # astronaut.flag = astronaut.countries.flag
    # astronaut.days = 3

    photo = astronaut.photo
    name = astronaut.name
    num_completed_flights = astronaut.num_completed_flights
    duration_completed_flights = astronaut.duration_completed_flights
    num_evas = astronaut.num_evas
    duration_evas = astronaut.duration_evas
    instagram = astronaut.instagram

    country = astronaut.countries
    flag = country.flag

    def current_flight_duration():
        """Calculate days in space for current flight"""

        current_flight_start = astronaut.current_flight_start
        start = datetime.strptime(current_flight_start, "%Y.%m.%d")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")

        delta = current - start

        days = delta.days

        return days

    days = current_flight_duration()

    return render_template("astronaut.html", #**astronaut.__dict__)
    
                            photo=photo,
                            name=name,
                            num_completed_flights=num_completed_flights,
                            duration_completed_flights=duration_completed_flights,
                            num_evas=num_evas,
                            duration_evas=duration_evas,
                            instagram=instagram,
                            flag=flag,
                            days=days)

#########################################################################

if __name__ == "__main__":
    # debug=True , since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run()
