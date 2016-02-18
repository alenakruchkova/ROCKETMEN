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

    # Number of people in space from JSON data
    num_result = jdict['number']

    # COLLECT list of names like ["Michael Kornienko", "Sergey Vokov",...] from JSON data
    name_list = [p['name'] for p in jdict['people']]

    #DB astronauts table query for names in name_list
    list_astro_obj = db.session.query(Astronaut).filter(Astronaut.name.in_(name_list)).all()

    def lookup_id_from_name(name):
        """Returns id corresponding to given astronaut's name"""

        for astronaut in list_astro_obj:
            if astronaut.name == name:
                return astronaut.astronaut_id
        return None

    name_id = {name: lookup_id_from_name(name) for name in name_list}

    return render_template("home.html",
                            num_result=num_result,
                            name_id=name_id)


@app.route("/astronauts/<int:astronaut_id>")
def show_astronaut_info(astronaut_id):
    """Show information about the astronaut"""

    #Query astronauts table on astronaut_id
    astronaut = Astronaut.query.filter(Astronaut.astronaut_id == astronaut_id).one()

    #From countries table get corresponding flag
    country = astronaut.countries
    flag = country.flag

    def current_flight_duration():
        """Calculate days in space for current flight"""

        #convert flight start date into a datetime obj
        current_flight_start = astronaut.current_flight_start
        start = datetime.strptime(current_flight_start, "%Y.%m.%d")

        #get current time datetime obj
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")

        #calculate delta, return days only
        delta = current - start
        days = delta.days
        return days

    days = current_flight_duration()

    return render_template("astronaut.html",
                            flag=flag,
                            days=days,
                            **astronaut.__dict__)

#######################################################################

@app.route('/astros.json')
def astronauts_info():
    """JSON info about people in space right now."""

    jdict = requests.get("http://api.open-notify.org/astros.json")
    jdict = jdict.json()

    return jsonify(jdict)

#########################################################################

if __name__ == "__main__":
    # debug=True , since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run()
