"""Utility file to seed ROCKETMEN database from Open Notify API data"""

from model import Country
from model import Astronaut

from model import connect_to_db, db
from server import app

from bs4 import BeautifulSoup
import urllib

######################

def load_astros_info():
    """Load astros info from astros.csv into database."""

    print "Astros Info"

    # Read astros.csv file and insert data
    for row in open("seed_data/astros.csv"):
        r = row.splitlines()
        print r

load_astros_info()
