import requests
from datetime import datetime
from googlemaps import Client
import os
from flask import request


#######################################################################

# API CALLS

def get_people_in_space_info():
    """Get data from API"""

    jdict = requests.get("http://api.open-notify.org/astros.json")
    jdict = jdict.json()

    return jdict


def get_current_iss_location():
    """Get JSON with current lat and lng of ISS from API"""

    jdict = requests.get("http://api.open-notify.org/iss-now.json")
    jdict = jdict.json()

    return jdict


def get_lat_lng():
    """ For user input (eg. 'Constitution Ave NW & 10th St NW, Washington, DC',

    'San Francisco, CA','Moscow, Russia')calculate geocode using Googlemaps API"""

    api_key = os.environ['GEOCODING_KEY']
    gmaps = Client(api_key)
    address = request.args.get("address")

    for dictionary in gmaps.geocode(address):
        lat = dictionary['geometry']['location']['lat']
        lng = dictionary['geometry']['location']['lng']

    payload = {'lat': lat,
               'lon': lng}

    return payload


def get_next_iss_pass_for_lat_lng():
    """ For lat lng calculate the next ISS pass"""
    # Based n user input get lat/lgn for address
    payload = get_lat_lng()

    # Get data from ISS pass API using payload
    result = requests.get("http://api.open-notify.org/iss-pass.json", params=payload)
    jdict = result.json()

    return jdict

######################################################################


def lookup_id_from_name(name, astronauts_list):
        """Returns id corresponding to given astronaut's name"""

        for astronaut in astronauts_list:
            if astronaut.name == name:
                return astronaut.astronaut_id
        return None


def look_up_flag(astronaut):
    """From countries table get corresponding flag"""

    country = astronaut.countries
    flag = country.flag

    return flag


def current_flight_duration(astronaut):
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
